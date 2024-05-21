import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, XSD

# Carregar o grafo RDF existente
g = Graph()
g.parse("med_doencas.ttl", format="turtle")

# Definir o namespace do seu grafo RDF
namespace = Namespace("http://www.example.org/disease-ontology#")

# Função para formatar URIs
def format_uri(name):
    return URIRef(namespace + name.strip().replace(" ", "_").replace(",", "").replace("'", ""))

# Função para adicionar uma instância de tratamento ao grafo RDF
def add_treatment_instance(treatment):
    treatment_uri = format_uri(treatment)
    if (treatment_uri, RDF.type, OWL.NamedIndividual) not in g:
        g.add((treatment_uri, RDF.type, OWL.NamedIndividual))
        g.add((treatment_uri, RDF.type, namespace.Treatment))
        g.add((treatment_uri, namespace.hasDescription, Literal(treatment, datatype=XSD.string)))

# Abrir o arquivo CSV Disease_Treatment.csv e ler os dados
with open("Disease_Treatment.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        disease_name = row["Disease"]
        treatments = [treatment.strip() for treatment in row.values() if treatment.strip() and treatment.strip() != disease_name]

        # Criar instâncias para cada tratamento, se ainda não existirem
        for treatment in treatments:
            treatment_uri = format_uri(treatment)
            if (None, None, treatment_uri) not in g:
                g.add((treatment_uri, RDF.type, OWL.NamedIndividual))
                g.add((treatment_uri, RDF.type, namespace.Treatment))

        # Associar cada doença aos respetivos tratamentos
        disease_uri = format_uri(disease_name)
        for treatment in treatments:
            treatment_uri = format_uri(treatment)
            g.add((disease_uri, namespace.hasTreatment, treatment_uri))

# Salvar o grafo RDF atualizado
g.serialize(destination="med_tratamentos.ttl", format="turtle")
