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

Mit Ihren Rückmeldungen können wir unser interaktives Lehrbuch gezielt an Ihre Bedürfnisse anpassen.
```
````


```{admonition} Achtung: Baustelle
:class: caution
Die hier beschriebenen Inhalte werden aktiv überarbeitet!
```

In diesem Kapitel wird Ihnen zuerst das Metadatenschema für QUADRIGA-OERs vorgestellt. Anschließend wird präsentiert, wie dieses in der Datei `metadata.yml` konkret umgesetzt wird. Zum Abschluss werden die tatsächlichen Metadaten der vorliegenden OER präsentiert.

## Das QUADRIGA Metadatenschema

Das QUADRIGA Metadatenschema basiert in Teilen auf DALIA[^url-dalia] sowie weiteren etablierten Metadatenstandards. Es wurde speziell für Open Educational Resources (OERs) entwickelt, die im Rahmen des QUADRIGA-Projekts erstellt werden und umfasst spezifische Felder zur Beschreibung von Lernzielen, Kompetenzen und didaktischen Elementen.

## Struktur und Felder der `metadata.yml`

Für die technische Umsetzung des Metadatenschemas wurde YAML[^url-yaml] gewählt, da es durch OER-Autor:innen einfach geschrieben und gleichzeitig gut automatisch verarbeitet werden kann.

Die Metadaten können theoretisch auch in anderen YAML-Dateien als eigenständiges YAML-Dokument eingebettet werden, jedoch empfehlen wir die Nutzung einer eigenständigen Datei. Komplexere Funktionalitäten von YAML wie Referenzen und Tags werden nicht genutzt.

Eine Metadatenbeschreibung nach dem QUADRIGA Metadatenschema wird als valide betrachtet, wenn sie mindestens alle Pflichtfelder beinhaltet und technisch korrekt umgesetzt wurde. Das Metadatenschema ist in JSON-Schema[^url-json-schema] implementiert. Das gesamte JSON-Schema der Metadaten ist [am Ende der Seite einzusehen](technologie:metadaten:json-schema)

Im Abschnitt Felder werden alle optionalen sowie verpflichtenden Felder präsentiert. Dabei wird jeweils angegeben, ob sie verpflichtend sind sowie welche Datentypen als Wert zugelassen sind.


### Struktur

Eine minimal kleine valide Metadatenbeschreibung sieht strukturell wie folgt aus:
```yaml
schema-version:
book-version:
title:
description:
  introduction:
  table-of-contents:
discipline:
duration:
type-of-research-object:
identifier:
url:
date-of-last-change:
publication-date:
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


### Felder
Im Folgenden werden die wichtigsten Felder des QUADRIGA-Metadatenschemas beschrieben. Pflichtfelder sind mit ⭐ gekennzeichnet.

(metadata:schema-version)=
#### `schema-version`⭐
Versionsnummer des QUADRIGA-Metadatenschemas. Es gibt ein kontrolliertes Vokabular möglicher Versionen (aktuell: "1.1", "1.1-beta", "1.1-beta2"). Wird das QUADRIGA-Metadatenschema verändert/erweitert, so wird eine neue Version in das kontrollierte Vokabular aufgenommen.

(metadata:book-version)=
#### `book-version`⭐
Version des Buchs im SemVer[^url-semver]-Format. Eine Versionsänderung korrespondiert auch immer mit einer Änderung von {ref}`metadata:date-of-last-change`.

(metadata:title)=
#### `title`⭐
Titel der OER.

(metadata:description)=
#### `description`⭐
Beschreibung der OER. Enthält die verpflichtenden Unterfelder Einleitung (`introduction`) und Inhaltsverzeichnis (`table-of-contents`).

(metadata:discipline)=
#### `discipline`⭐
Nennung der Disziplinen, die bei der Erstellung der OER im Fokus standen. Mögliche Disziplinen sind in einem kontrollierten Vokabular definiert.

(metadata:duration)=
#### `duration`⭐
Angedachte Bearbeitungsdauer für Lernende.

(metadata:type-of-research-object)=
#### `type-of-research-object`⭐
Nennung des Datentyps, der vorrangig in der OER behandelt wird. Es können ein bis zwei Typen aus einem kontrollierten Vokabular ausgewählt werden.

(metadata:identifier)=
#### `identifier`⭐
Eindeutiger Identifier in Form einer DOI. Die DOI identifiziert das gesamte Buch.

(metadata:url)=
#### `url`⭐
URL der Website-Ansicht des Buchs.

(metadata:git)=
#### `git`
Git-Repositorium, in dem die OER-Inhalte zu finden sind.

(metadata:has-predecessor)=
#### `has-predecessor`
Link zur Vorgänger-OER oder `false`. Verweis auf eine Vorgänger-OER, in der z.B. vorausgesetzte Inhalte erklärt werden.

(metadata:has-successor)=
#### `has-successor`
Link zur Nachfolger-OER oder `false`. Verweis auf eine Nachfolger-OER, in der z.B. Inhalte aus der aktuellen OER weiterentwickelt werden.

(metadata:date-of-last-change)=
#### `date-of-last-change`⭐
Datum der letzten (großen, inhaltlich umfangreichen) Änderung. Sollte immer mit einer Versionsänderung ({ref}`metadata:book-version`) einhergehen.

(metadata:publication-date)=
#### `publication-date`⭐
Datum der Erstveröffentlichung.

(metadata:target-group)=
#### `target-group`⭐
Zielgruppe des Buchs. Es können eine oder mehrere Zielgruppen aus einem kontrollierten Vokabular ausgewählt werden.

(metadata:authors)=
#### `authors`⭐
Liste der Autor:innen der OER. Das Feld ist verpflichtend und es muss mindestens ein:e Autor:in in der Liste aufgeführt werden. Eine Autor:in wird entweder als einfache Zeichenkette oder strukturiert mit mindestens Vor- und Nachnamen angegeben, optional mit ORCID und weiteren Informationen.

(metadata:chapters)=
#### `chapters`⭐
Liste der Kapitel des Buchs. Jedes Kapitel enthält einen Titel ({ref}`metadata:chapter-title`), eine Beschreibung ({ref}`metadata:chapter-description`), eine Liste von Lernzielen ({ref}`metadata:learning-objectives`) und ein Groblernziel ({ref}`metadata:learning-goal`). Optional können auch eine URL zum direkten Zugriff auf die Kapitelseite und eine Bearbeitungsdauer angegeben werden.

(metadata:learning-objectives)=
#### `learning-objectives`⭐ (in `chapters`)
Eine Liste von Lernzielen. Jedes Lernziel umfasst eine Formulierung des Lernziels (`learning-objective`), die adressierte Kompetenz ({ref}`metadata:competency`), einen Kompetenz-Fokus ({ref}`metadata:focus`), eine Einordnung im Datenfluss ({ref}`metadata:data-flow`) und eine Kategorie aus der Bloomschen Taxonomie (`blooms-category`).

(metadata:learning-goal)=
#### `learning-goal`⭐ (in `chapters`)
Kurze Benennung des Groblernziels des Kapitels.

(metadata:context-of-creation)=
#### `context-of-creation`⭐
Eine Beschreibung des Entstehungskontextes. Im konkreten Fall ein natürlichsprachlicher Verweis auf das QUADRIGA-Projekt.

(metadata:keywords)=
#### `keywords`
Liste von Schlag-/Stichwörtern, welche das Buch und dessen (Lern-)Inhalte beschreiben.

(metadata:language)=
#### `language`
Sprache der OER als ISO639-1 Sprachcode.

(metadata:license)=
#### `license`
Lizenz des Buchs und des Codes jeweils als URL oder als Kombination aus Lizenzname und URL. Mindestens die Informationen zur Lizenz des Inhalts (`content`) sind erforderlich, optional können auch Angaben zur Lizenz des Codes (`code`) gemacht werden.

(metadata:prerequisites)=
#### `prerequisites`
Liste von Voraussetzungen und deren jeweiliger Einordnung in der Bloomschen Taxonomie, welche Lernende für die erfolgreiche Bearbeitung des Buchs mitbringen sollten.

(metadata:quality-assurance)=
#### `quality-assurance`
Eine Liste von Qualitätssicherungs-Ereignissen. Jedes Ereignis enthält eine Person, ein Datum und optional eine Beschreibung der durchgeführten Qualitätssicherungsmaßnahme.

(metadata:related-works)=
#### `related-works`
Eine Liste von Verweisen und jeweils einer kurzen Beschreibung zu zusätzlichen, weiterführenden OERs. Jeder Eintrag enthält eine Beschreibung (`description`) und einen Link (`url`).

(metadata:supplemented-by)=
#### `supplemented-by`
Liste von Verweisen und jeweils einer kurzen Beschreibung zu zusätzlichen, weiterführenden Inhalten o.ä., die in einem Kapitel verwendet werden. Jeder Eintrag enthält eine Beschreibung (`description`) und eine URL (`url`).

(metadata:type-of-learning-resource)=
#### `type-of-learning-resource`
Beschreibung der Materialart der OER. Aktuell ist nur "Jupyter Book" als Wert vorgesehen.

(metadata:used-tools)=
#### `used-tools`
Liste von Tools, die bei der Erstellung des Buchs verwendet wurden. Diese können als einfache URI oder als strukturierte Angabe mit Namen und URL angegeben werden.

(metadata:data-flow)=
#### `data-flow`⭐ (in `learning-objectives`)
Schritt im Datenfluss, dem die Kompetenz zugeordnet ist. Muss aus einem kontrollierten Vokabular ausgewählt werden: "Grundlagen", "Planung", "Erhebung und Aufbereitung", "Management", "Analyse" sowie "Publikation und Nachnutzung".

(metadata:competency)=
#### `competency`⭐ (in `learning-objectives`)
Im Lernziel adressierte Kompetenz nach dem QUADRIGA Datenkompetenzframework. Muss aus einem kontrollierten Vokabular ausgewählt werden.

(metadata:blooms-category)=
#### `blooms-category`⭐ (in `learning-objectives`)
Kategorie der Bloomschen Taxonomie, welcher das Lernziel zugeordnet ist. Aus der Kombination der Zuordnungen der Lernziele eines Kapitels lässt sich ein allgemeines Kompetenzniveau ("Basis", "Fortgeschritten", "Expert:in") ableiten. Muss aus einem kontrollierten Vokabular ausgewählt werden.

(metadata:focus)=
#### `focus`⭐ (in `learning-objectives`)
Fokus des Lernziels auf den Aspekt "Wissen", "Fähigkeit" oder "Haltung" der Kompetenz.

<!-- Fields defined in $defs follow below -->

(metadata:semver)=
#### `semver`
Ein Bezeichner nach dem Semantic Versioning 2.0.0 Format[^url-semver]. Wird bei der Versionierung des Schemas und der OER verwendet. Besteht aus Major-, Minor- und Patch-Version (z.B. "1.1.0"), optional gefolgt von Pre-Release-Identifikatoren und Build-Metadaten.

(metadata:multilingual-text)=
#### `multilingual-text`
Natürlichsprachlicher Text wird standardmäßig auf Deutsch verfasst. Soll dies explizit gemacht werden und/oder sollen andere Sprachen verwendet werden, so kann hier statt einer Zeichenkette (`string`) ein Mapping (`object`) von ISO639-1 Sprachcodes und dem Text in der entsprechenden Sprache verwendet werden.

(metadata:person)=
#### `person`
Eine Person kann entweder als einfache Zeichenkette oder als Mapping, das mindestens Schlüssel für Vor- und Nachname (`given-names`, `family-names`) enthält modelliert werden.

Es wird empfohlen eine ORCID[^url-orcid] anzugeben. Zusätzlich können Rollen nach dem CRediT-System (Contributor Roles Taxonomy) für die Person angegeben werden.

(metadata:chapter-title)=
#### `title`⭐ (in `chapters`)
Kapitelüberschrift, die für dieses Kapitel verwendet wird. Kann als einfacher Text oder als mehrsprachiger Text angegeben werden.

(metadata:chapter-description)=
#### `description`⭐ (in `chapters`)
Beschreibung des Kapitelinhalts. Bietet eine Übersicht darüber, was in diesem Kapitel behandelt wird.

(metadata:chapter-url)=
#### `url` (in `chapters`)
URL zum direkten Zugriff auf die erste Seite der 'Leseansicht' (Website) des Kapitels.

(metadata:chapter-duration)=
#### `duration` (in `chapters`)
Angedachte Bearbeitungsdauer für Lernende, spezifisch für dieses Kapitel.

## `metadata.yml` der vorliegenden OER

```{literalinclude} /metadata.yml
:language: yaml
:linenos:
```

(technologie:metadaten:json-schema)=
## JSON-Schema[^url-json-schema]
```{literalinclude} /quadriga-schema.json
:language: json
:linenos:
```

[^url-yaml]: <https://yaml.org>
[^url-json-schema]: <https://json-schema.org>
[^url-dalia]: <https://dalia.education>
[^url-semver]: <https://semver.org>
[^url-orcid]: <https://orcid.org>