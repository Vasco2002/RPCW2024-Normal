import pandas as pd
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, RDFS, XSD

# Definir o namespace do seu grafo RDF
namespace = Namespace("http://www.example.org/disease-ontology#")

# Carregar o grafo RDF existente
g = Graph()
g.parse("medical.ttl", format="turtle")

# Adicionar propriedades e classes se ainda não existirem
def add_property(prop, domain, range_):
    if (prop, None, None) not in g:
        g.add((prop, RDF.type, OWL.ObjectProperty))
        g.add((prop, RDFS.domain, domain))
        g.add((prop, RDFS.range, range_))

def add_datatype_property(prop, domain, range_):
    if (prop, None, None) not in g:
        g.add((prop, RDF.type, OWL.DatatypeProperty))
        g.add((prop, RDFS.domain, domain))
        g.add((prop, RDFS.range, range_))

def add_class(cls):
    if (cls, None, None) not in g:
        g.add((cls, RDF.type, OWL.Class))

# Adicionar classes
add_class(namespace.Disease)
add_class(namespace.Symptom)
add_class(namespace.Treatment)
add_class(namespace.Patient)

# Adicionar propriedades
has_symptom = URIRef(namespace + "hasSymptom")
has_description = URIRef(namespace + "hasDescription")

add_property(has_symptom, namespace.Disease, namespace.Symptom)
add_datatype_property(has_description, namespace.Disease, XSD.string)

# Função para formatar URIs
def format_uri(name):
    return URIRef(namespace + name.strip().replace(" ", "_").replace(",", "").replace("'", ""))

# Ler o arquivo Disease_Syntoms.csv
df_syntoms = pd.read_csv("Disease_Syntoms.csv")

# Processar sintomas e doenças
for index, row in df_syntoms.iterrows():
    disease_name = row['Disease']
    disease_uri = format_uri(disease_name)
    
    # Adicionar a doença se ainda não existir
    if (disease_uri, RDF.type, namespace.Disease) not in g:
        g.add((disease_uri, RDF.type, OWL.NamedIndividual))
        g.add((disease_uri, RDF.type, namespace.Disease))
    
    # Processar os sintomas
    for symptom in row[1:].dropna():
        symptom_uri = format_uri(symptom)
        
        # Adicionar o sintoma se ainda não existir
        if (symptom_uri, RDF.type, namespace.Symptom) not in g:
            g.add((symptom_uri, RDF.type, OWL.NamedIndividual))
            g.add((symptom_uri, RDF.type, namespace.Symptom))
        
        # Associar o sintoma à doença
        g.add((disease_uri, has_symptom, symptom_uri))

# Ler o arquivo Disease_Description.csv
df_description = pd.read_csv("Disease_Description.csv")

# Processar descrições de doenças
for index, row in df_description.iterrows():
    disease_name = row['Disease']
    description = row['Description']
    disease_uri = format_uri(disease_name)
    
    # Adicionar a descrição à instância da doença se a doença existir
    if (disease_uri, RDF.type, namespace.Disease) in g:
        g.add((disease_uri, has_description, Literal(description, datatype=XSD.string)))

# Salvar o grafo atualizado
g.serialize("med_doencas.ttl", format="turtle")
