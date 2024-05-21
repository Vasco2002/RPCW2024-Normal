import json
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, XSD

# Carregar o grafo RDF existente
g = Graph()
g.parse("med_tratamentos.ttl", format="turtle")

# Definir o namespace do seu grafo RDF
namespace = Namespace("http://www.example.org/disease-ontology#")

# Função para formatar URIs
def format_uri(name):
    return URIRef(namespace + name.strip().replace(" ", "_").replace(",", "").replace("'", ""))

# Abrir o arquivo JSON e ler os dados
with open("pg54269.json", "r") as json_file:
    patients = json.load(json_file)

# Iterar sobre cada paciente no arquivo JSON e adicionar as informações ao grafo RDF
for idx, patient in enumerate(patients):
    patient_id = "p" + str(idx + 1)  # Gerar um ID para o paciente
    patient_uri = format_uri(patient_id)
    g.add((patient_uri, RDF.type, OWL.NamedIndividual))
    g.add((patient_uri, RDF.type, namespace.Patient))
    g.add((patient_uri, namespace.name, Literal(patient['nome'])))  # Adicionar o nome do paciente

    # Adicionar os sintomas associados ao paciente
    for symptom in patient['sintomas']:
        symptom_uri = format_uri(symptom)
        g.add((patient_uri, namespace.exhibitsSymptom, symptom_uri))

# Serializar e salvar o grafo RDF atualizado
g.serialize(destination="med_doentes.ttl", format="turtle")
