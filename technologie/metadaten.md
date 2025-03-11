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

Das QUADRIGA Metadatenschema basiert in Teilen auf DALIA[^url-dalia] sowie …

## Struktur und Felder der `metadata.yml`

Für die technische Umsetzung des Metadatenschemas wurde YAML[^url-yaml] gewählt, da es durch OER-Autor:innen einfach geschrieben und gleichzeitig gut automatisch verarbeitet werden kann.

Die Metadaten können theoretisch auch in anderen YAML-Dateien als eigenständiges YAML-Dokument eingebettet werden, jedoch empfehlen wir die Nutzung einer eigenständigen Datei. Komplexere Funktionalitäten von YAML wie Referenzen und Tags werden nicht genutzt.

Eine Metadatenbeschreibung nach dem QUADRIGA Metadatenschema wird als valide betrachtet, wenn sie mindestens alle Pflichtfelder beinhaltet und technisch korrekt umgesetzt wurde. Das Metadatenschema ist in JSON-Schema[^url-json-schema] implementiert. Das gesamte JSON-Schema der Metadaten ist [am Ende der Seite einzusehen](technologie:metadaten:json-schema)

Im Abschnitt Felder werden alle optionalen sowie verpflichtenden Felder präsentiert. Dabei wird jeweils angegeben, ob sie verpflichtend sind sowie welche Datentypen als Wert zugelassen sind.


### Struktur

Eine minimal kleine valide Metadatenbeschreibung sieht strukturell wie folgt aus:
```yaml
schema-version: "1.1"
oer-version:
identifier:
title:
description:
authors:
git:
context-of-creation:
date-of-last-change:
publication-date:
discipline:
target-group:
duration:
has-predecessor:
has-successor:
type-of-research-object:
learning-objectives:
  - learning-objective:
    competency:
    data-flow:
    blooms-category:
chapters:
  - description:
    title:
    learning-objectives:
      - learning-objective:
        competency:     
        data-flow:
        blooms-category:
```


### Felder
… hier noch eine menschenlesbare Beschreibung …

#### `authors`
`authors` ist eine Liste der Autor:innen der OER. Das Feld ist verpflichtend und es muss mindestens ein:e Autor:in in der Liste aufgeführt werden. Eine Autor:in ist modelliert als [`person`](person).

#### `chapters`
Liste der Kapitel der OER. Sie muss mindestens ein Kapitel enthalten. Ein Kapitel wird mit einem Titel (`title`), einer Beschreibung (`description`) einer Liste von Lernzielen ([`learning-objectives`](learning-objectives)) sowie ggf. einer DOI und einer URL beschrieben.

#### `context-of-creation` (Umbenennung in `context-of-development`?)
Eine Beschreibung des Entstehungskontextes. Im konkreten Fall ein natürlichsprachlicher ([`multilingual-text`](multilingual-text)) Verweis auf das QUADRIGA-Projekt.

#### `date-of-last-change`
Datum der letzten (großen, inhaltlich umfangreichen) Änderung. Sollte immer mit einer Versionsänderung ([`oer-version`](oer-version)) einhergehen.

#### `description`
Die Beschreibung der OER beinhaltet einerseits das Inhaltsverzeichnis und andererseits einen einleitenden Text. Beide sind als [`multilingual-text`](multilingual-text) modelliert.

#### `discipline`
In diesem Feld werden alle Disziplinen aufgezählt, welche bei der Erstellung der OER im Fokus standen. Es gibt ein kontrolliertes Vokabular möglicher Disziplinen.

#### `duration`
In diesem Feld wird angegeben, wie lange Lernende ca. für das Bearbeiten der OER brauchen.

#### `git`
Verweis auf das Git-Repositorium, in dem die OER zu finden ist.

#### `has-predecessor`
Verweis auf eine Vorgänger-OER, in der bspw. vorausgesetzte Inhalte erklärt oder vorangegangene Schritte durchgeführt werden. Entweder `false` oder der [`identifier`](identifier) des Vorgängers.

Hat OER A einen Vorgänger B, so verweist B im Eintrag [`has-successor`](has-successor) auf A.

#### `has-successor`
Verweis auf eine Nachfolger-OER, in der bspw. Inhalte oder Ergebnisse aus der aktuellen OER nachgenutzt/weiterentwickelt werden. Entweder `false` oder der [`identifier`](identifier) des Nachfolgers.

Hat OER A einen Nachfolger B, so verweist B im Eintrag [`has-predecessor`](has-predecessor) auf A.

#### `identifier`
Eindeutiger Identifier in Form einer DOI. Die DOI identifiziert die gesamte OER.

#### `keywords`
Eine Liste von Stichwörtern oder Schlagwörtern.

#### `language`
Sprache der OER als ISO639-1 Sprachcode.

#### `learning-objectives`
Liste der Lernziele einer OER bzw. eines Kapitels. Ein Lernziel selbst besteht aus einer genauen Formulierung des Lernziels (`learning-objective`), der zugeordneten Kompetenz (`competency`) und eine Einordnung in eine Kategorie aus der Bloomschen Taxonomie (`blooms-category`).

#### `license`
Verweis auf die verwendet(en) Lizenz(en).

#### `multilingual-text`
Natürlichsprachlicher Text wird standardmäßig auf Deutsch verfasst. Soll dies explizit gemacht werden und/oder sollen andere Sprachen verwendet werden, so kann hier statt einer Zeichenkette (`string`) ein Mapping (`object`) von ISO639-1 Sprachcodes und dem Text in der entsprechenden Sprache verwendet werden.

#### `oer-version`
Version der OER im SemVer[^url-semver]-Format. Eine Versionsänderung korrespondiert auch immer mit einer Änderung von [`date-of-last-change`](date-of-last-change).

#### `person`
Eine Person kann entweder als einfache Zeichenkette oder als Mapping, das mindestens Schlüssel für Vor- und Nachname (`given-names`, `family-names`) enthält modelliert werden.

Es wird empfohlen eine ORCID anzugeben.

#### `prerequisites`
Liste der Vorkenntnisse, die für ein erfolgreiches bearbeiten der OER angenommen werden.

#### `publication-date`
Datum der Erstveröffentlichung.

#### `quality-assurance`
Informationen zum Qualitätsmanagement (QM, engl.: quality assurance (QA)) werden hier hinterlegt. Diese sind eine Liste von QM-Ereignissen, welche jeweils beschrieben werden mit einer Person ([`person`](person)), dem Datum des QM-Ereignisses sowie ggf. einer Beschreibung (`description`) der durchgeführten QM-Maßnahme und ggf. deren Ergebnisse.

#### `related-work`
Eine Liste von Verweisen (URL, o.ä.) und jeweils einer kurzen Beschreibung zu zusätzlichen, weiterführenden Inhalten o.ä.

#### `schema-version`
Versionsnummer des QUADRIGA-Metadatenschemas im SemVer[^url-semver]-Format. Es gibt ein kontrolliertes Vokabular möglicher Versionen. Wird das QUADRIGA-MEtadatenschema verändert/erweitert, so wird einen neue Version in das kontrollierte Vokabular aufgenommen.

#### `target-group`
Beschreibung der Zielgruppe der OER. Es können eine oder mehrere Zielgruppen aus einem kontrollierten Vokabular ausgewählt werden.

#### `title`
Titel der OER.

#### `type-of-learning-resource`
Beschreibung der Materialart der OER. Auswahl aus einem kontrollierten Vokabular.

#### `type-of-research-object`
Bis zu zwei Datentyp, welche in der OER im Fokus stehen können aus einem kontrollierten Vokabular ausgewählt werden. 

#### `url`
URL der "Leseansicht" der OER.

#### `used-tools`
Verweise auf genutzte Software nach LCSH.


## `metadata.yml` der vorliegenden OER

```{literalinclude} ../metadata.yml
:language: yaml
:linenos:
```

(technologie:metadaten:json-schema)=
## JSON-Schema[^url-json-schema]
```{literalinclude} ../quadriga-schema.json
:language: json
:linenos:
```

[^url-yaml]: <https://yaml.org>
[^url-json-schema]: <https://json-schema.org>
[^url-dalia]: <https://dalia.education>
[^url-semver]: <https://semver.org>