---
lang: de-DE
---

(technologie:metadaten)=
# Metadaten

````{margin}
```{admonition} Fragen oder Feedback 
:class: frage-feedback

<a href="https://github.com/quadriga-dk/Book_Template/issues/new?assignees=&labels=question&projects=&template=frage.yml" class="external-link" target="_blank">
    Stellen Sie eine Frage
</a> <br>
<a href="https://github.com/quadriga-dk/Book_Template/issues/new?assignees=&labels=feedback&projects=&template=feedback.yml" class="external-link" target="_blank">
    Geben Sie uns Feedback
</a>

Mit Ihren Rückmeldungen können wir unser Jupyter Book gezielt an Ihre Bedürfnisse anpassen.
```
````


```{admonition} Feinlernziele
:class: lernziele
1. Lernende kennen das Metadatenschema für in QUADRIGA erstellte OERs und dessen technische Umsetzung.
2. Lernende können die Metadaten ihrer eigenen OER dem QUADRIGA-Schema entsprechend umsetzen.
```

In diesem Kapitel wird Ihnen zuerst das Metadatenschema für QUADRIGA-OERs vorgestellt. Anschließend wird präsentiert, wie dieses in der Datei `metadata.yml` konkret umgesetzt wird. Zum Abschluss werden die tatsächlichen Metadaten der vorliegenden OER präsentiert.

## Das QUADRIGA Metadatenschema+

Das QUADRIGA Metadatenschema basiert in Teilen auf DALIA[^url-dalia] sowie …

## Struktur und Felder der `metadata.yml`

Für die technische Umsetzung des Metadatenschemas wurde YAML[^url-yaml] gewählt, da es durch OER-Autor\*innen einfach geschrieben und gleichzeitig gut automatisch verarbeitet werden kann.

Die Metadaten können theoretisch auch in anderen YAML-Dateien als eigenständiges YAML-Dokument eingebettet werden, jedoch empfehlen wir die Nutzung einer eigenständigen Datei. Komplexere Funktionalitäten von YAML wie Referenzen und Tags werden nicht genutzt.

Eine Metadatenbeschreibung nach dem QUADRIGA Metadatenschema wird als valide betrachtet, wenn sie mindestens alle Pflichtfelder beinhaltet und technisch korrekt umgesetzt wurde. Das Metadatenschema ist in JSON-Schema[^url-json-schema] implementiert.

Im Abschnitt Felder werden alle optionalen sowie verpflichtenden Felder präsentiert. Dabei wird jeweils angegeben, ob sie verpflichtend sind sowie welche Datentypen als Wert zugelassen sind.


### Struktur

Eine minimal kleine valide Metadatenbeschreibung sieht strukturell wie folgt aus:
```yaml
schema-version:
title:
description:
doi:
git:
learning-objectives:
  - learning-objective:
    competency:
children:
  - learning-objective:
    title:
    learning-objectives:
      - learning-objective:
        competency: 
```


### Felder
… hier noch eine menschenlesbare Beschreibung …

### JSON-Schema[^url-json-schema]
```{literalinclude} ../quadriga-schema.json
:language: json
:linenos:
```

## `metadata.yml` der vorliegenden OER

```{literalinclude} ../metadata.yml
:language: yaml
:linenos:
```


[^url-yaml]: <https://yaml.org>
[^url-json-schema]: <https://json-schema.org>
[^url-dalia]: <https://dalia.education>