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
        uri_odrl = "http://www.w3.org/ns/odrl/2/"
        uri_csvw = "http://www.w3.org/ns/csvw#"
        uri_foaf = "http://xmlns.com/foaf/0.1/"

        g = graph

        g.parse("ontology/EDAAnOWL.ttl", format="turtle")
        
        #######################
        #                     #
        #      Catálogo       #
        #                     #
        #######################

        uri_catalogo = (
            uri_edaan + "catalog" + catalogo["@id"].capitalize().replace("-", "_")
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
                    rdflib.Literal(catalogo["dct:title"]),
                )
            )
        
        g.add(
                (
                    rdflib.URIRef(uri_catalogo),
                    rdflib.URIRef(uri_dct + "description"),
                    rdflib.Literal(catalogo["dct:description"]),
                )
            )
        
        g.add(
                (
                    rdflib.URIRef(uri_catalogo),
                    rdflib.URIRef(uri_dct + "issued"),
                    rdflib.Literal(catalogo["dct:issued"]),
                )
            )
        
        g.add(
                (
                    rdflib.URIRef(uri_catalogo),
                    rdflib.URIRef(uri_dct + "publisher"),
                    rdflib.Literal(catalogo["dct:publisher"]),
                )
            )

        ##########################
        #                        #
        #      Data assets       #
        #                        #
        ##########################

        for dataasset in catalogo["dcat:dataset"]:
            uri_dataasset = (
                uri_edaan
                + str(dataasset["@id"]).capitalize().replace("-","_")
            )

            type_dataasset1 = uri_dcat + "dataset"
            type_dataasset2 = uri_idsa + "Resource"

            g.add(
                (
                    rdflib.URIRef(uri_catalogo),
                    rdflib.URIRef(uri_dcat + "data_asset"),
                    rdflib.URIRef(uri_dataasset),
                )
            )
            g.add(
                (
                    rdflib.URIRef(uri_dataasset),
                    RDF.type,
                    rdflib.URIRef(type_dataasset1),
                )
            )
            g.add(
                (
                    rdflib.URIRef(uri_dataasset),
                    RDF.type,
                    rdflib.URIRef(type_dataasset2),
                )
            )
            if(dataasset.get("dcat:version")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dcat + "version"),
                        rdflib.Literal(dataasset["dcat:version"]),
                    )
                )
            if(dataasset.get("dct:title")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dct + "title"),
                        rdflib.Literal(dataasset["dct:title"]),
                    )
                )
            if(dataasset.get("dct:description")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dct + "description"),
                        rdflib.Literal(dataasset["dct:description"]),
                    )
                )
            if(dataasset.get("accessType")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_edaan + "accesstype"),
                        rdflib.Literal(dataasset["accessType"]),
                    )
                )
            if(dataasset.get("isAlive")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_edaan + "isAlive"),
                        rdflib.Literal(dataasset["isAlive"]),
                    )
                )
            if(dataasset.get("dcat:keyword")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dcat + "keyword"),
                        rdflib.Literal(dataasset["dcat:keyword"]),
                    )
                )
            if(dataasset.get("topicTags")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_edaan + "topicTags"),
                        rdflib.Literal(dataasset["topicTags"]),
                    )
                )
            if(dataasset.get("dct:publisher")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dct + "publisher"),
                        rdflib.Literal(dataasset["dct:publisher"]),
                    )
                )
            if(dataasset.get("dct:creator")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dct + "creator"),
                        rdflib.Literal(dataasset["dct:creator"]),
                    )
                )
            if(dataasset.get("ids:sovereign")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_idsa + "sovereign"),
                        rdflib.Literal(dataasset["ids:sovereign"]),
                    )
                )
            if(dataasset.get("ids:contactPoint")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_idsa + "contactPoint"),
                        rdflib.Literal(dataasset["ids:contactPoint"]),
                    )
                )
            if(dataasset.get("dct:theme")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dct + "theme"),
                        rdflib.Literal(dataasset["dct:theme"]),
                    )
                )
            if(dataasset.get("dct:spatial")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dct + "spatial"),
                        rdflib.Literal(dataasset["dct:spatial"]),
                    )
                )
            if(dataasset.get("dct:temporal")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dct + "temporal"),
                        rdflib.Literal(dataasset["dct:temporal"]),
                    )
                )
            if(dataasset.get("dct:language")):
                for lang in dataasset["dct:language"]:
                    g.add(
                        (
                            rdflib.URIRef(uri_dataasset),
                            rdflib.URIRef(uri_dct + "language"),
                            rdflib.Literal(lang),
                        )
                    )
            if(dataasset.get("dct:issued")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dct + "issued"),
                        rdflib.Literal(dataasset["dct:issued"]),
                    )
                )
            if(dataasset.get("dct:modified")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dct + "modified"),
                        rdflib.Literal(dataasset["dct:modified"]),
                    )
                )
            if(dataasset.get("ids:provenance")):
                uri_provenance = uri_edaan + "provenance"
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_idsa + "provenance"),
                        rdflib.URIRef(uri_provenance),
                    )
                )
                g.add(
                    (
                        rdflib.URIRef(uri_provenance),
                        RDF.type,
                        rdflib.URIRef(uri_idsa),
                    )
                )
                if(dataasset["ids:provenance"].get("resource")):
                    g.add(
                        (
                            rdflib.URIRef(uri_provenance),
                            rdflib.URIRef(uri_edaan + "resource"),
                            rdflib.Literal(dataasset["ids:provenance"]["resource"]),
                        )
                    )
                if(dataasset["ids:provenance"].get("collectionMethod")):
                    g.add(
                        (
                            rdflib.URIRef(uri_provenance),
                            rdflib.URIRef(uri_edaan + "collectionMethod"),
                            rdflib.Literal(dataasset["ids:provenance"]["collectionMethod"]),
                        )
                    )
                if(dataasset["ids:provenance"].get("fieldProvenance")):
                    g.add(
                        (
                            rdflib.URIRef(uri_provenance),
                            rdflib.URIRef(uri_edaan + "fieldProvenance"),
                            rdflib.Literal(dataasset["ids:provenance"]["fieldProvenance"]),
                        )
                    )
            if(dataasset.get("dataUtility")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_edaan + "dataUtility"),
                        rdflib.Literal(dataasset["dataUtility"]),
                    )
                )
            if(dataasset.get("dct:license")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_dct + "license"),
                        rdflib.Literal(dataasset["dct:license"]),
                    )
                )
            if(dataasset.get("securityPrivacy")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_edaan + "securityPrivacy"),
                        rdflib.Literal(dataasset["securityPrivacy"]),
                    )
                )
            if(dataasset.get("ids:representation")):
                for representation in dataasset["ids:representation"]:
                    uri_representation = uri_edaan + str(representation["@id"]).capitalize().replace("-","_")
                    g.add(
                        (
                            rdflib.URIRef(uri_dataasset),
                            rdflib.URIRef(uri_idsa + "representation"),
                            rdflib.URIRef(uri_representation),
                        )
                    )
                    g.add(
                        (
                            rdflib.URIRef(uri_representation),
                            RDF.type,
                            rdflib.URIRef(uri_idsa + "Representation"),
                        )
                    )
                    if(representation.get("dcat:mediaType")):
                        g.add(
                            (
                                rdflib.URIRef(uri_representation),
                                rdflib.URIRef(uri_dcat + "mediaType"),
                                rdflib.Literal(representation["dcat:mediaType"]),
                            )
                        )
                    if(representation.get("ids:representationStandard")):
                        g.add(
                            (
                                rdflib.URIRef(uri_representation),
                                rdflib.URIRef(uri_idsa + "representationStandard"),
                                rdflib.Literal(representation["ids:representationStandard"]),
                            )
                        )
                    if(representation.get("encoding")):
                        g.add(
                            (
                                rdflib.URIRef(uri_representation),
                                rdflib.URIRef(uri_edaan + "encoding"),
                                rdflib.Literal(representation["encoding"]),
                            )
                        )
                    if(representation.get("csvw:dialect")):
                        g.add(
                            (
                                rdflib.URIRef(uri_representation),
                                rdflib.URIRef(uri_csvw + "dialect"),
                                rdflib.Literal(representation["csvw:dialect"]),
                            )
                        )
                    if(representation.get("ids:instance")):
                        for instance in representation["ids:instance"]:
                            uri_artifact = uri_edaan + instance["@id"]
                            g.add(
                                (
                                    rdflib.URIRef(uri_representation),
                                    rdflib.URIRef(uri_idsa + "instance"),
                                    rdflib.URIRef(uri_artifact),
                                )
                            )
                            g.add(
                                (
                                    rdflib.URIRef(uri_artifact),
                                    RDF.type,
                                    rdflib.URIRef(uri_idsa + "Artifact"),
                                )
                            )
                            if(instance.get("ids:fileName")):
                                g.add(
                                    (
                                        rdflib.URIRef(uri_artifact),
                                        rdflib.URIRef(uri_idsa + "fileName"),
                                        rdflib.Literal(instance["ids:fileName"]),
                                    )
                                )
                            if(instance.get("ids:byteSize")):
                                g.add(
                                    (
                                        rdflib.URIRef(uri_artifact),
                                        rdflib.URIRef(uri_idsa + "byteSize"),
                                        rdflib.Literal(instance["ids:byteSize"]),
                                    )
                                )
                            if(instance.get("ids:checkSum")):
                                g.add(
                                    (
                                        rdflib.URIRef(uri_artifact),
                                        rdflib.URIRef(uri_idsa + "checkSum"),
                                        rdflib.Literal(instance["ids:checkSum"])
                                    )
                                )
                            if(instance.get("ids:creationDate")):
                                g.add(
                                    (
                                        rdflib.URIRef(uri_artifact),
                                        rdflib.URIRef(uri_idsa + "creationDate"),
                                        rdflib.Literal(instance["ids:creationDate"]),
                                    )
                                )
            if(dataasset.get("ids:contractOffer")):
                for contract in dataasset["ids:contractOffer"]:
                    uri_contract = uri_edaan + contract["@id"]
                    g.add(
                        (
                            rdflib.URIRef(uri_dataasset),
                            rdflib.URIRef(uri_idsa + "contractOffer"),
                            rdflib.URIRef(uri_contract),
                        )
                    )
                    g.add(
                        (
                            rdflib.URIRef(uri_contract),
                            RDF.type,
                            rdflib.URIRef(uri_idsa + "ContractOffer"),
                        )
                    )
                    if(contract.get("dct:title")):
                        g.add(
                            (
                                rdflib.URIRef(uri_contract),
                                rdflib.URIRef(uri_dct + "title"),
                                rdflib.Literal(contract["dct:title"]),
                            )
                        )
                    if(contract.get("odrl:hasPolicy")):
                        uri_hasPolicy = uri_edaan + "hasPolicy"
                        g.add(
                            (
                                rdflib.URIRef(uri_contract),
                                rdflib.URIRef(uri_odrl + "hasPolicy"),
                                rdflib.URIRef(uri_hasPolicy),
                            )
                        )
                        g.add(
                            (
                                rdflib.URIRef(uri_hasPolicy),
                                RDF.type,
                                rdflib.URIRef(uri_odrl + "hasPolicy"),
                            )
                        )
                        if(contract["odrl:hasPolicy"].get("odrl:permission")):
                            g.add(
                                (
                                    rdflib.URIRef(uri_hasPolicy),
                                    rdflib.URIRef(uri_odrl + "permission"),
                                    rdflib.Literal(contract["odrl:hasPolicy"]["odrl:permission"]),
                                )
                            )
                        if(contract["odrl:hasPolicy"].get("odrl:obligation")):
                            g.add(
                                (
                                    rdflib.URIRef(uri_hasPolicy),
                                    rdflib.URIRef(uri_odrl + "obligation"),
                                    rdflib.Literal(contract["odrl:hasPolicy"]["odrl:obligation"]),
                                )
                            )
            if(dataasset.get("dcat:distribution")):
                for distribution in dataasset["dcat:distribution"]:
                    uri_distribution = uri_edaan + distribution["@id"]
                    g.add(
                        (
                            rdflib.URIRef(uri_dataasset),
                            rdflib.URIRef(uri_dcat + "distribution"),
                            rdflib.URIRef(uri_distribution),
                        )
                    )
                    g.add(
                        (
                            rdflib.URIRef(uri_distribution),
                            RDF.type,
                            rdflib.URIRef(uri_dcat + "Distribution"),
                        )
                    )
                    if(distribution.get("dcat:accessURL")):
                        g.add(
                            (
                                rdflib.URIRef(uri_distribution),
                                rdflib.URIRef(uri_dcat + "accessURL"),
                                rdflib.URIRef(distribution["dcat:accessURL"]),
                            )
                        )
                    if(distribution.get("dct:title")):
                        g.add(
                            (
                                rdflib.URIRef(uri_distribution),
                                rdflib.URIRef(uri_dct + "title"),
                                rdflib.Literal(distribution["dct:title"]),
                            )
                        )
            if(dataasset.get("extraQualityMetadata")):
                g.add(
                    (
                        rdflib.URIRef(uri_dataasset),
                        rdflib.URIRef(uri_edaan + "extraQualityMetadata"),
                        rdflib.Literal(dataasset["extraQualityMetadata"]),
                    )
                )
        

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
                "catalog" in file
                and ".json" in file
                and "annotation.schema.json" not in file
            ):
                
                (graph_rdf(os.path.join(root, file), g, schema))

    owl_file = open(
        "output_triples.ttl",
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