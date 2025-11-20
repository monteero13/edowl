import json
import jsonschema
import rdflib
import os
import uuid
from rdflib import Graph, RDFS, RDF
from jsonschema import validate


def graph_rdf(path: str, graph, schema) -> Graph:
    """
    Read to json file (path) and return a graph object with the information of the json file

    Args:
        path (str): The path to the JSON file.
        graph: The graph object to add information to.
        schema: The JSON schema to validate the file against.

    Returns:
        Graph: The graph object with information from the file added.
    """
    try:
        error_in_modelage = 0
        # open json file
        with open(path, "r") as f:
            catalogo = json.load(f)

        try:
            validate(catalogo, schema)
            result = path + " follows the schema."
        except jsonschema.exceptions.ValidationError as e:
            result = path + f" --> ERROR does not follow the schema : {e}"
            error_in_modelage += 1

        with open("log_annotation.txt", "a") as file:
            file.write(result + "\n")

        uri_edaan = "http://www.ontologies.khaos.uma.es/edaan/"
        uri_bigowl = "http://www.ontologies.khaos.uma.es/bigowl/"
        uri_idsa = "https://w3id.org/idsa/core/"
        uri_dcat = "http://www.w3.org/ns/dcat#"
        uri_dct   = "http://purl.org/dc/terms/"


        g = graph
        
        #######################
        #                     #
        #      Catálogo       #
        #                     #
        #######################

        uri_catalogo = (
            uri_edaan + "catalog" + catalogo["@id"].capitalize().replace(" ", "_")
        )
        type_catalog = uri_dcat + "Catalog"
        
        g.add(
                (
                    rdflib.URIRef(uri_catalogo),
                    RDF.type,
                    rdflib.URIRef(type_catalog),
                )
            )
        
        g.add(
                (
                    rdflib.URIRef(uri_catalogo),
                    rdflib.URIRef(uri_dct + "title"),
                    rdflib.URIRef(rdflib.Literal(catalogo["dct:title"])),
                )
            )
        
        g.add(
                (
                    rdflib.URIRef(uri_catalogo),
                    rdflib.URIRef(uri_dct + "description"),
                    rdflib.URIRef(rdflib.Literal(catalogo["dct:description"])),
                )
            )
        
        g.add(
                (
                    rdflib.URIRef(uri_catalogo),
                    rdflib.URIRef(uri_dct + "issued"),
                    rdflib.URIRef(rdflib.Literal(catalogo["dct:issued"])),
                )
            )

        ##########################
        #                        #
        #      Data assets       #
        #                        #
        ##########################

        
        if error_in_modelage != 1:
            g = graph

    except Exception as e:
        print("ERROR: " + str(e))
        print(
            "NOTE: if ontology was changed, please change list_parametre_type in main.py"
        )
        print(
            "Please check " + os.getcwd() + "/log_annotation.txt " + "for more errors"
        )
        print("\n")

        g = graph

    return g


def main(schema):
    g = Graph()

    with open("log_annotation.txt", "w") as file:
        file.write("Annotation.json Schema Compliance \n\n")
    p = 0
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if (
                "annotation" in file
                and ".json" in file
                and "annotation.schema.json" not in file
            ):
                p += 1
                (graph_rdf(os.path.join(root, file), g, schema))
    print("Number of components: ", p, "\n")

    owl_file = open(
        "ontology/EDAAnOWL.owl",
        "w",
    )
    owl_file.write(g.serialize(format="nt"))
    owl_file.close()


if __name__ == "__main__":
    __version__ = "0.2.1"
    __group__ = "Khaos Research <khaos.uma.es>"

    HEADER = "\n".join(
        [
            r"  _____ ____    _    _    _   _ ",
            r" | ____|  _ \  / \  / \  | \ | |",
            r" |  _| | | | |/ _ \/ _ \ |  \| |",
            r" | |___| |_| / ___ \ ___ \| |\  |",
            r" |_____|____/_/   \_\_/   \_\_| \_|",
            "                                   ",
            f" Ver. {__version__}  Group. {__group__}  ",
            "                                   ",
        ]
    )

    print(HEADER)
    # open json schema file
    with open("annotation.schema.json", "r") as f:
        schema = json.load(f)

    main(schema)