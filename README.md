# Semantic Data Annotator & RDF Generator

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

Este proyecto es una herramienta de automatización diseñada para la **ingesta, validación y transformación semántica** de catálogos de datos. 

El script toma metadatos descritos en formato JSON, los valida contra un esquema estricto y los transforma en un **Grafo de Conocimiento (Knowledge Graph)** basado en estándares como **DCAT, IDS, Dublin Core y ODRL**, integrando los nuevos datos sobre una ontología base (`EDAAnOWL`).

## 🚀 Funcionalidades

- **Validación de Esquema:** Utiliza `jsonschema` para asegurar que los archivos de entrada (`catalog.json`) cumplen con la estructura esperada (`annotation.schema.json`).
- **Carga de Ontología Base:** Importa una ontología preexistente en formato Turtle (`.ttl`) para mantener la coherencia del modelo de datos.
- **Mapeo Semántico (ETL):** Transforma objetos JSON y listas anidadas (datasets, distribuciones, contratos, políticas) en tripletas RDF.
- **Soporte Multilingüe:** Manejo de literales con etiquetas de idioma (es/en).
- **Generación de Grafo:** Exporta el resultado combinado (Ontología + Datos) en formato estándar N-Triples (`.nt`) o Turtle (`.ttl`).

## 📂 Estructura del Proyecto

El sistema espera la siguiente organización de archivos para funcionar correctamente:

```text
.
├── annotation.schema.json    # Esquema JSON para validar la estructura de entrada
├── catalog_*.json            # Archivos de entrada con los metadatos (Data Assets)
├── main.py                   # Script principal de ejecución
├── pyproject.toml            # Configuración de dependencias (uv / poetry)
├── ontology/
│   └── EDAAnOWL.ttl          # Ontología base (Input)
├── output_triples.nt         # Grafo resultante generado (Output)
└── README.md                 # Documentación del proyecto