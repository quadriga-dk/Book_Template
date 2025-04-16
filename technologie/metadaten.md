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


```{admonition} Feinlernziele
:class: lernziele
1. Lernende kennen das Metadatenschema für in QUADRIGA erstellte OERs und dessen technische Umsetzung.
2. Lernende können die Metadaten ihrer eigenen OER dem QUADRIGA-Schema entsprechend umsetzen.
```

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
Version der OER im SemVer[^url-semver]-Format. Eine Versionsänderung korrespondiert auch immer mit einer Änderung von {ref}`metadata:date-of-last-change`.

(metadata:title)=
#### `title`⭐
Titel der OER.

(metadata:description)=
#### `description`⭐
Die Beschreibung der OER enthält eine Einleitung (`introduction`) und ein Inhaltsverzeichnis (`table-of-contents`). Beide Felder sind erforderlich.

(metadata:discipline)=
#### `discipline`
In diesem Feld werden alle Disziplinen aufgezählt, welche bei der Erstellung der OER im Fokus standen. Es gibt ein kontrolliertes Vokabular möglicher Disziplinen.

(metadata:duration)=
#### `duration`⭐
In diesem Feld wird angegeben, wie lange Lernende ca. für das Bearbeiten der OER brauchen.

(metadata:type-of-research-object)=
#### `type-of-research-object`⭐
Bis zu zwei Datentypen, welche in der OER im Fokus stehen, können aus einem kontrollierten Vokabular ausgewählt werden. Mögliche Werte sind "Text", "Tabelle", "Bewegtes Bild" und "übergreifend".

(metadata:identifier)=
#### `identifier`⭐
Eindeutiger Identifier in Form einer DOI. Die DOI identifiziert die gesamte OER.

(metadata:url)=
#### `url`⭐
URL der "Leseansicht" der OER.

(metadata:git)=
#### `git`
Verweis auf das Git-Repositorium, in dem die OER zu finden ist.

(metadata:has-predecessor)=
#### `has-predecessor`
Verweis auf eine Vorgänger-OER, in der bspw. vorausgesetzte Inhalte erklärt oder vorangegangene Schritte durchgeführt werden. Entweder `false` oder der {ref}`metadata:identifier` des Vorgängers.

Hat OER A einen Vorgänger B, so verweist B im Eintrag {ref}`metadata:has-successor` auf A.

(metadata:has-successor)=
#### `has-successor`
Verweis auf eine Nachfolger-OER, in der bspw. Inhalte oder Ergebnisse aus der aktuellen OER nachgenutzt/weiterentwickelt werden. Entweder `false` oder der {ref}`metadata:identifier` des Nachfolgers.

Hat OER A einen Nachfolger B, so verweist B im Eintrag {ref}`metadata:has-predecessor` auf A.

(metadata:date-of-last-change)=
#### `date-of-last-change`⭐
Datum der letzten (großen, inhaltlich umfangreichen) Änderung. Sollte immer mit einer Versionsänderung ({ref}`metadata:book-version`) einhergehen.

(metadata:publication-date)=
#### `publication-date`⭐
Datum der Erstveröffentlichung.

(metadata:target-group)=
#### `target-group`⭐
Beschreibung der Zielgruppe der OER. Es können eine oder mehrere Zielgruppen aus einem kontrollierten Vokabular ausgewählt werden.

(metadata:authors)=
#### `authors`⭐
`authors` ist eine Liste der Autor:innen der OER. Das Feld ist verpflichtend und es muss mindestens ein:e Autor:in in der Liste aufgeführt werden. Eine Autor:in wird entweder als einfache Zeichenkette oder strukturiert mit mindestens Vor- und Nachnamen angegeben, optional mit ORCID und weiteren Informationen.

(metadata:chapters)=
#### `chapters`⭐
Liste der Kapitel der OER. Sie muss mindestens ein Kapitel enthalten. Ein Kapitel wird mit einem Titel (`title`), einer Beschreibung (`description`), einem Groblernziel (`learning-goal`), einer Liste von Lernzielen ({ref}`metadata:learning-objectives`) sowie ggf. einer URL und weiteren Informationen beschrieben.

(metadata:learning-objectives)=
#### `learning-objectives`⭐
Liste der Lernziele eines Kapitels. Ein Lernziel selbst besteht aus einer genauen Formulierung des Lernziels (`learning-objective`), der zugeordneten Kompetenz ({ref}`metadata:competency`), dem Kompetenz-Fokus des Lernziels ({ref}`metadata:focus`), einer Einordnung in den Datenfluss ({ref}`metadata:data-flow`) und eine Einordnung in eine Kategorie aus der Bloomschen Taxonomie ({ref}`metadata:blooms-category`).

(metadata:context-of-creation)=
#### `context-of-creation`⭐
Eine Beschreibung des Entstehungskontextes. Im konkreten Fall ein natürlichsprachlicher Verweis auf das QUADRIGA-Projekt.

(metadata:keywords)=
#### `keywords`
Eine Liste von Stichwörtern oder Schlagwörtern.

(metadata:language)=
#### `language`
Sprache der OER als ISO639-1 Sprachcode.

(metadata:license)=
#### `license`
Verweis auf die verwendete(n) Lizenz(en). Bei Angabe sind mindestens Informationen zur Lizenz des Inhalts (`content`) erforderlich, optional können auch Angaben zur Lizenz des Codes (`code`) gemacht werden.

(metadata:prerequisites)=
#### `prerequisites`
Liste der Vorkenntnisse, die für ein erfolgreiches bearbeiten der OER angenommen werden.

(metadata:quality-assurance)=
#### `quality-assurance`
Informationen zum Qualitätsmanagement (QM, engl.: quality assurance (QA)) werden hier hinterlegt. Diese sind eine Liste von QM-Ereignissen, welche jeweils beschrieben werden mit einer Person ({ref}`metadata:person`), dem Datum des QM-Ereignisses sowie ggf. einer Beschreibung (`description`) der durchgeführten QM-Maßnahme und ggf. deren Ergebnisse.

(metadata:related-works)=
#### `related-works`
Eine Liste von Verweisen (URL, o.ä.) und jeweils einer kurzen Beschreibung zu zusätzlichen, weiterführenden Inhalten o.ä.

(metadata:type-of-learning-resource)=
#### `type-of-learning-resource`
Beschreibung der Materialart der OER. Auswahl aus einem kontrollierten Vokabular.

(metadata:used-tools)=
#### `used-tools`
Verweise auf genutzte Software nach LCSH. Diese können als einfache URI oder als strukturierte Angabe mit Namen und URL angegeben werden.

(metadata:data-flow)=
#### `data-flow`
Stufe im Datenfluss nach dem QUADRIGA Datenkompetenzframework. Wird bei der Beschreibung von Lernzielen verwendet und kann aus einem kontrollierten Vokabular ausgewählt werden: "Grundlagen", "Planung", "Erhebung und Aufbereitung", "Management", "Analyse" sowie "Publikation und Nachnutzung".

(metadata:competency)=
#### `competency`
Im Lernziel adressierte Kompetenz nach dem QUADRIGA Datenkompetenzframework. Wird bei der Beschreibung von Lernzielen verwendet und kann aus einem kontrollierten Vokabular ausgewählt werden.

(metadata:blooms-category)=
#### `blooms-category`
Einordnung eines Lernziels in eine Kategorie aus der Bloomschen Taxonomie. Wird bei der Beschreibung von Lernzielen verwendet und kann aus einem kontrollierten Vokabular ausgewählt werden.

(metadata:focus)=
#### `focus`
Fokus eines Lernziels auf den Aspekt "Wissen", "Fähigkeit" oder "Haltung" der Kompetenz.

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