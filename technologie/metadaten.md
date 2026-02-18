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

Mit Ihren Rückmeldungen können wir unser interaktives Lehrbuch gezielt an Ihre Bedürfnisse anpassen.
```
````

In diesem Kapitel wird Ihnen zuerst das Metadatenschema für QUADRIGA-OERs
vorgestellt. Anschließend wird präsentiert, wie dieses in der Datei
`metadata.yml` konkret umgesetzt wird. Zum Abschluss werden die tatsächlichen
Metadaten der vorliegenden OER präsentiert sowie die verschiedenen
Exportformate erläutert.

## Das QUADRIGA Metadatenschema

Das QUADRIGA Metadatenschema wurde speziell für Open Educational Resources
(OERs) entwickelt, die im Rahmen des QUADRIGA-Projekts erstellt werden und
umfasst spezifische Felder zur Beschreibung von Lernzielen, Kompetenzen und
didaktischen Elementen. Dazu kombiniert es verschiedene Metadatenstandards wie
<a href="http://purl.org/dc/elements/1.1" target="_blank"
    class="external-link">Dublin Core Elements 1.1</a>, <a
    href="http://purl.org/dc/terms/" target="_blank"
    class="external-link">Dublin Core Terms</a>, <a href="https://schema.org"
    target="_blank" class="external-link">schema.org</a>, <a
    href="http://purl.org/dcx/lrmi-terms/" target="_blank"
    class="external-link">LRMI</a> und <a
    href="https://purl.org/ontology/modalia#" target="_blank"
    class="external-link">MoDALIA</a> (siehe auch <a
    href="https://dalia.education" target="_blank"
    class="external-link">DALIA</a>). Hierzu werden Mappings unter Verwendung
von <a href="https://www.w3.org/TR/skos-reference/#L4160" target="_blank"
    class="external-link">skos:mappingRelation</a> definiert.

## Struktur und Felder der `metadata.yml`

Für die Definition der Metadaten im Jupyter Book wurde <a
    href="https://yaml.org" target="_blank" class="external-link">YAML</a>
gewählt, da es durch OER-Autor:innen einfach geschrieben und gleichzeitig gut
automatisch verarbeitet werden kann.

Die Metadaten können theoretisch auch in anderen YAML-Dateien als
eigenständiges YAML-Dokument eingebettet werden, jedoch setzen die Skripte zur
automatischen Generierung von Formaten wie <a
    href="https://citation-file-format.github.io" target="_blank"
    class="external-link">CFF</a>, <a href="https://www.bibtex.org"
    target="_blank" class="external-link">BibTeX</a> und anderen die
Speicherung der Metadaten in der Datei `metadata.yml` im Wurzelverzeichnis des
Jupyter Book voraus.

Eine Metadatenbeschreibung nach dem QUADRIGA Metadatenschema wird als valide
betrachtet, wenn sie mindestens alle Pflichtfelder beinhaltet und technisch
korrekt umgesetzt wurde. Das Metadatenschema ist in <a
    href="https://json-schema.org" target="_blank"
    class="external-link">JSON-Schema</a> implementiert und zu finden in auf
GitHub (<a href="https://github.com/quadriga-dk/quadriga-schema"
    target="_blank"
    class="external-link">https://github.com/quadriga-dk/quadriga-schema</a>)
und als <a href="https://quadriga-dk.github.io/quadriga-schema/"
    target="_blank" class="external-link">HTML-Darstellung</a>. Die
`.json`-Dateien der Schemadefinition (<a
    href="https://quadriga-dk.github.io/quadriga-schema/v1.0.0/schema.json"
    target="_blank" class="external-link">bspw. `schema.json` der Version
1.0.0</a>) sind ebenfalls auf der GitHub Page publiziert und können darüber
eingebunden werden.

Im Abschnitt Felder werden alle optionalen sowie verpflichtenden Felder
präsentiert. Dabei wird jeweils angegeben, ob sie verpflichtend sind sowie
welche Datentypen als Wert zugelassen sind.

### Struktur

Eine minimal kleine valide Metadatenbeschreibung sieht strukturell wie folgt
aus:

```yaml
schema-version:
version:
title:
description:
table-of-contents:
discipline:
time-required:
research-object-type:
identifier:
url:
date-modified:
date-issued:
target-group:
authors:
    - given-names:
      family-names:
chapters:
    - title:
      description:
      learning-objectives:
          - learning-objective:
            competency:
            focus:
            data-flow:
            blooms-category:
      learning-goal:
context-of-creation:
```

Eine <a
    href="https://github.com/quadriga-dk/quadriga-schema/blob/main/minimal_metadata.yml"
    target="_blank" class="external-link">minimale Metadatendatei als
Startpunkt</a> finden Sie ebenfalls im <a
    href="https://github.com/quadriga-dk/quadriga-schema/" target="_blank"
    class="external-link">Repositorium zum QUADRIGA-Metadaten-Schema</a>.

### Felder

Im Folgenden werden die wichtigsten Felder des QUADRIGA-Metadatenschemas
beschrieben. Pflichtfelder sind mit ⭐ gekennzeichnet. Nutzen Sie auch die <a
    href="https://quadriga-dk.github.io/quadriga-schema" target="_blank"
    class="external-link">interaktive Darstellung des Schemas</a>.

(metadata:schema-version)=

#### `schema-version`⭐

Versionsnummer des QUADRIGA-Metadatenschemas. Es gibt ein kontrolliertes
Vokabular möglicher Versionen (aktuell: "1.0.0"). Wird das
QUADRIGA-Metadatenschema verändert/erweitert, so wird eine neue Version
definiert. Vorherige, veröffentlichte Versionen bleiben bestehen, können jedoch
ggf. als "deprecated" markiert werden.

(metadata:version)=

#### `version`⭐

Version des Buchs im <a href="https://semver.org" target="_blank"
    class="external-link">SemVer</a>-Format. Eine Versionsänderung
korrespondiert auch immer mit einer Änderung von {ref}`metadata:date-modified`.

(metadata:title)=

#### `title`⭐

Titel der OER.

(metadata:description)=

#### `description`⭐

Beschreibung der OER als Freitext.

(metadata:table-of-contents)=

#### `table-of-contents`⭐

Inhaltsverzeichnis der OER als Freitext.

(metadata:discipline)=

#### `discipline`⭐

Nennung der Disziplinen, die bei der Erstellung der OER im Fokus standen.
Mögliche Disziplinen sind in einem kontrollierten Vokabular definiert.

(metadata:time-required)=

#### `time-required`⭐

Angedachte Bearbeitungsdauer für Lernende im ISO 8601 Duration-Format (siehe <a
    href="https://en.wikipedia.org/wiki/ISO_8601#Durations" target="_blank"
    class="external-link">Wikipedia-Artikel zu ISO8601</a>).

Beispiele:

- `PT16H15M` für 16 Stunden und 15 Minuten
- `P1DT10S` für 1 Tag und 10 Sekunden

Typischerweise werden Angaben zur Bearbeitungsdauer in Stunden und Minuten
angegeben.

(metadata:research-object-type)=

#### `research-object-type`⭐

Nennung des Datentyps, der vorrangig in der OER behandelt wird. Es können ein
bis zwei Typen aus einem kontrollierten Vokabular ausgewählt werden.

(metadata:identifier)=

#### `identifier`⭐

Eindeutiger Identifier in Form einer DOI. Die DOI identifiziert das gesamte
Buch.

(metadata:url)=

#### `url`⭐

URL der Website-Ansicht des Buchs.

(metadata:git)=

#### `git`

Git-Repositorium, in dem die OER-Inhalte zu finden sind.

(metadata:has-predecessor)=

#### `has-predecessor`

Link zur Vorgänger-OER oder `false`. Verweis auf eine Vorgänger-OER, in der
z.B. vorausgesetzte Inhalte erklärt werden.

(metadata:has-successor)=

#### `has-successor`

Link zur Nachfolger-OER oder `false`. Verweis auf eine Nachfolger-OER, in der
z.B. Inhalte aus der aktuellen OER weiterentwickelt werden.

(metadata:date-modified)=

#### `date-modified`⭐

Datum der letzten (großen, inhaltlich umfangreichen) Änderung. Sollte immer mit
einer Versionsänderung ({ref}`metadata:version`) einhergehen. Verbesserungen
von Grammatik und Orthographie verlangen nicht zwingend die Erstellung einer
neuen Version. Dieses Datum muss jedoch aktualisiert werden, wenn eine neue
Version auf Zenodo veröffentlicht wird (bspw. über die Release-Funktion auf
GitHub).

(metadata:date-issued)=

#### `date-issued`⭐

Datum der Erstveröffentlichung.

(metadata:target-group)=

#### `target-group`⭐

Zielgruppe des Buchs. Es können eine oder mehrere Zielgruppen aus einem
kontrollierten Vokabular ausgewählt werden.

(metadata:authors)=

#### `authors`⭐

Liste der Autor:innen der OER. Das Feld ist verpflichtend und es muss
mindestens ein:e Autor:in in der Liste aufgeführt werden. Eine Autor:in wird
entweder als einfache Zeichenkette oder strukturiert mit mindestens Vor- und
Nachnamen angegeben, optional mit ORCID und weiteren Informationen.

Eine strukturierte Angabe der Informationen zu eine:r Autor:in wird empfohlen.

(metadata:chapters)=

#### `chapters`⭐

Liste der Kapitel des Buchs. Jedes Kapitel enthält einen Titel
({ref}`metadata:chapter-title`), eine Beschreibung
({ref}`metadata:chapter-description`), eine Liste von Lernzielen
({ref}`metadata:learning-objectives`) und ein Groblernziel
({ref}`metadata:learning-goal`). Optional können auch eine URL zum direkten
Zugriff auf die Kapitelseite und eine Bearbeitungsdauer angegeben werden.

(metadata:learning-objectives)=

#### `learning-objectives`⭐ (in `chapters`)

Eine Liste von Lernzielen. Jede Lernzieldefinition umfasst eine Formulierung
des Lernziels (`learning-objective`), die adressierte Kompetenz
({ref}`metadata:competency`), eine Einordnung im Datenfluss
({ref}`metadata:data-flow`) und eine Kategorie aus der Bloomschen Taxonomie
(`blooms-category`).

(metadata:learning-goal)=

#### `learning-goal`⭐ (in `chapters`)

Kurze Benennung des Groblernziels des Kapitels.

(metadata:context-of-creation)=

#### `context-of-creation`⭐

Eine Beschreibung des Entstehungskontextes. Im konkreten Fall ein
natürlichsprachlicher Verweis auf das QUADRIGA-Projekt.

(metadata:keywords)=

#### `keywords`

Liste von Schlag-/Stichwörtern, welche das Buch und dessen (Lern-)Inhalte
beschreiben.

(metadata:language)=

#### `language`

Sprache der OER als ISO639-1 Sprachcode (zwei Buchstaben – bspw. `de`, `en`,
…).

(metadata:license)=

#### `license`

Lizenz des Buchs und des Codes jeweils als URL oder als Kombination aus
Lizenzname und URL. Mindestens die Informationen zur Lizenz des Inhalts
(`content`) sind erforderlich, optional können auch Angaben zur Lizenz des
Codes (`code`) gemacht werden.

(metadata:prerequisites)=

#### `prerequisites`

Liste von Voraussetzungen und deren jeweiliger Einordnung in der Bloomschen
Taxonomie, welche Lernende für die erfolgreiche Bearbeitung des Buchs
mitbringen sollten.

(metadata:quality-assurance)=

#### `quality-assurance`

Eine Liste von Qualitätssicherungs-Ereignissen. Jedes Ereignis enthält eine
Person, ein Datum und optional eine Beschreibung der durchgeführten
Qualitätssicherungsmaßnahme.

_Dieses Feld wird aktuell noch überarbeitet!_

(metadata:related-works)=

#### `related-works`

Eine Liste von Verweisen und jeweils einer kurzen Beschreibung zu zusätzlichen,
weiterführenden OERs. Jeder Eintrag enthält eine Beschreibung (`description`)
und einen Link (`url`).

(metadata:supplemented-by)=

#### `supplemented-by`

Liste von Verweisen und jeweils einer kurzen Beschreibung zu zusätzlichen,
weiterführenden Inhalten o.ä., die in einem Kapitel verwendet werden. Jeder
Eintrag enthält eine Beschreibung (`description`) und eine URL (`url`).

(metadata:type-of-learning-resource)=

#### `type-of-learning-resource`

Beschreibung der Materialart der OER. Aktuell ist nur "Jupyter Book" als Wert
vorgesehen.

(metadata:used-tools)=

#### `used-tools`

Liste von Tools, die bei der Erstellung des Buchs verwendet wurden. Diese
können als einfache URI oder als strukturierte Angabe mit Namen und URL
angegeben werden.

(metadata:data-flow)=

#### `data-flow`⭐ (in `learning-objectives`)

Schritt im Datenfluss, dem die Kompetenz zugeordnet ist. Muss aus einem
kontrollierten Vokabular ausgewählt werden: "Grundlagen", "Planung", "Erhebung
und Aufbereitung", "Management", "Analyse" sowie "Publikation und Nachnutzung".

(metadata:competency)=

#### `competency`⭐ (in `learning-objectives`)

Im Lernziel adressierte Kompetenz nach dem QUADRIGA Datenkompetenzframework.
Muss aus einem kontrollierten Vokabular ausgewählt werden.

(metadata:blooms-category)=

#### `blooms-category`⭐ (in `learning-objectives`)

Kategorie der Bloomschen Taxonomie, welcher das Lernziel zugeordnet ist. Aus
der Kombination der Zuordnungen der Lernziele eines Kapitels lässt sich ein
allgemeines Kompetenzniveau ("Basis", "Fortgeschritten", "Expert:in") ableiten.
Muss aus einem kontrollierten Vokabular ausgewählt werden.

(metadata:semver)=

#### `semver`

Ein Bezeichner nach dem <a href="https://semver.org" target="_blank"
    class="external-link">Semantic Versioning 2.0.0 Format</a>. Wird bei der
Versionierung des Schemas und der OER verwendet. Besteht aus Major-, Minor- und
Patch-Version (z.B. "1.1.0"), optional gefolgt von Pre-Release-Identifikatoren
und Build-Metadaten.

(metadata:multilingual-text)=

#### `multilingual-text`

Natürlichsprachlicher Text wird standardmäßig auf Deutsch verfasst. Soll dies
explizit gemacht werden und/oder sollen andere Sprachen verwendet werden, so
kann hier statt einer Zeichenkette (`string`) ein Mapping (`object`) von
ISO639-1 Sprachcodes und dem Text in der entsprechenden Sprache verwendet
werden.

(metadata:person)=

#### `person`

Eine Person kann entweder als einfache Zeichenkette oder als Mapping, das
mindestens Schlüssel für Vor- und Nachname (`given-names`, `family-names`)
enthält modelliert werden.

Es wird empfohlen eine <a href="https://orcid.org" target="_blank"
    class="external-link">ORCID</a> anzugeben. Zusätzlich können Rollen nach
dem CRediT-System (Contributor Roles Taxonomy) für die Person angegeben werden.

(metadata:chapter-title)=

#### `title`⭐ (in `chapters`)

Kapitelüberschrift, die für dieses Kapitel verwendet wird. Kann als einfacher
Text oder als mehrsprachiger Text angegeben werden.

(metadata:chapter-description)=

#### `description`⭐ (in `chapters`)

Beschreibung des Kapitelinhalts. Bietet eine Übersicht darüber, was in diesem
Kapitel behandelt wird.

(metadata:chapter-url)=

#### `url` (in `chapters`)

URL zum direkten Zugriff auf die erste Seite der 'Leseansicht' (Website) des
Kapitels.

(metadata:chapter-time-required)=

#### `time-required` (in `chapters`)

Angedachte Bearbeitungsdauer für Lernende, spezifisch für dieses Kapitel, im
ISO 8601 Duration-Format.

## `metadata.yml` der vorliegenden OER

```{literalinclude} /metadata.yml
:language: yaml
:linenos:
```

(technologie:metadaten:json-schema)=

## <a href="https://json-schema.org" target="_blank" class="external-link">JSON-Schema</a>

Das JSON-Schema ist definiert im Repositorium <a
    href="https://github.com/quadriga-dk/quadriga-schema" target="_blank"
    class="external-link">quadriga-schema</a>. Auf Basis dieses Repositoriums
wird eine <a href="https://quadriga-dk.github.io/quadriga-schema/schema.html"
    target="_blank" class="external-link">interaktive Darstellung</a> sowie der
<a href="https://quadriga-dk.github.io/quadriga-schema/latest/schema.json"
    target="_blank" class="external-link">Einstieg für die Nutzung in anderen
Schemas oder in Verifikationstools (`schema.json` hier im Versionsalias
`latest`)</a> generiert. Für die Verwendung in Werkzeugen sollte immer eine
bestimmte Version festgelegt werden – bspw.
<https://quadriga-dk.github.io/quadriga-schema/v1.0.0/schema.json>

(technologie:metadaten:export-formate)=

## Metadaten-Exportformate

Die in `metadata.yml` erfassten Metadaten werden automatisch in verschiedene
standardisierte Formate exportiert, um die Auffindbarkeit, Nachnutzbarkeit und
Interoperabilität der OER zu gewährleisten. Die Transformation erfolgt durch
Python-Skripte im Verzeichnis `quadriga/metadata/` und wird im Build-Prozess
automatisch ausgeführt.

### Generierte Formate

(technologie:metadaten:json-ld)=

#### JSON-LD (`metadata.jsonld`)

<a href="https://json-ld.org" target="_blank" class="external-link">JSON-LD
(JavaScript Object Notation for Linked Data)</a> ist ein Format für
strukturierte, verlinkte Daten im Web. Die exportierten Metadaten folgen dem
Schema.org-Vokabular und werden als maschinenlesbare Linked Data
bereitgestellt.

Im Publikationsprozess werden per GitHub Action die JSON-LD-Daten in die
Startseite des Buchs sowie die Kapitel-Startseiten integriert.

(technologie:metadaten:rdf)=

#### RDF/XML (`metadata.rdf`)

<a href="https://www.w3.org/RDF/" target="_blank" class="external-link">RDF
(Resource Description Framework)</a> in XML-Serialisierung ermöglicht die
Verarbeitung der Metadaten durch Semantic-Web-Anwendungen und Triple Stores.

Ein `<link>`-Tag zu den RDF-Daten wird über die GitHub Action in die Startseite
des Buchs integriert.

(technologie:metadaten:bibtex)=

#### BibTeX (`references.bib`)

BibTeX-Format für die Referenzen, auf welche sich im Buch berufen wird.

(technologie:metadaten:citation-cff)=

#### CITATION.cff

GitHub-Standard für Software- und Datensatz-Zitation im CITATION.cff-Format
(Citation File Format).

(technologie:metadaten:zenodo)=

#### Zenodo JSON (`.zenodo.json`)

Metadaten im Zenodo-Format für die Archivierung und DOI-Vergabe über die
Zenodo-Plattform. Diese Metadaten liefern die Grundlage für die Metadaten in
Zenodo.

Das Format ist definiert in <a
    href="https://github.com/zenodo/zenodo/blob/482ee72ad501cbbd7f8ce8df9b393c130d1970f7/zenodo/modules/deposit/jsonschemas/deposits/records/legacyrecord.json"
    target="_blank" class="external-link">`legacyrecord.json`</a>.

### Metadaten-Verarbeitungspipeline

Die Verarbeitung der Metadaten erfolgt in folgenden Schritten:

1. **Quelldateien**: `metadata.yml` mit QUADRIGA-Schema (siehe
   {ref}`metadata:schema-version`) sowie `_config.yml` und `_toc.yml` Im ersten
   Schritt werden ggf. Informationen (bspw. Titel des Buchs, Inhaltsverzeichnis,
   …) in `metadata.yml` auf Basis der Jupyter Book Konfigurationsdateien
   aktualisiert.
2. **Generierung**: Python-Skripte in `quadriga/metadata/` transformieren die
   YAML-Daten:
    - `create_jsonld.py` → `metadata.jsonld`
    - `create_rdfxml.py` → `metadata.rdf`
    - `create_bibtex.py` → `references.bib`
    - `update_citation_cff.py` → `CITATION.cff`
    - `create_zenodo_json.py` → `.zenodo.json`
3. **Build**: Jupyter Book erstellt die HTML-Ausgabe in `_build/html/`
4. **Injektion**: `inject_metadata.py` bettet JSON-LD in HTML-Seiten ein und
   fügt RDF-Links hinzu
5. **Bereitstellung**: Relevante Metadatendateien werden in das
   Build-Verzeichnis kopiert

Die Skripte nutzen gemeinsame Hilfsfunktionen aus `utils.py` für
YAML-Verarbeitung, Keyword-Extraktion und Formatierung.
