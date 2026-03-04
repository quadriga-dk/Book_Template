---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.18.1
kernelspec:
  display_name: SPARQL
  language: sparql
  name: sparql
---

# SPARQL Beispiel

Neben Jupyter Notebooks können auch Markdown-Dateien ausführbaren Code enthalten. Dazu muss ein korrekter Vorspann ("frontmatter") vorhanden sein, in dem per `kernelspec` ein Jupyter Kernel für das Notebook definiert wird. Hier wird der SPARQL-Kernel geladen.

Basierend auf der OER https://quadriga-dk.github.io/Tabelle-Fallstudie-2/SPARQL_Grundlagen.html als minimaler Test der SPARQL-Einbindung.

```{code-cell} sparql
%endpoint https://data.europa.eu/sparql
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dcatde: <http://dcat-ap.de/def/dcatde/>
PREFIX pg: <https://www.dcat-ap.de/def/politicalGeocoding/>

SELECT ?uri ?title ?contributorid ?stateKey
WHERE {
    ?uri dct:title ?title .
    ?uri dcatde:contributorID ?contributorid .
  OPTIONAL {?uri pg:stateKey ?stateKey} .
}
```

