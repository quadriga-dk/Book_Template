---
lang: de-DE
---

# QUADRIGA OERs: erstellen und gestalten mit Jupyter Book

Open Educational Resources (OER) ermöglichen die Erarbeitung, Verbesserung, Aktualisierung und Nutzung von Lehr- und Lerninhalten in einer breiten Community innerhalb klarer rechtlicher Regelungen einer offenen Lizenzierung.

Um diese Aktivitäten möglichst einfach zu gestalten und gleichzeitig die langfristige Nutzbarkeit unabhängig von bestimmten Technologien zu ermöglichen werden OERs im Rahmen des QUADRIGA-Projekts basierend auf Markdown-Dateien und Jupyter-Notebooks erstellt, für die eine langfristige Nutzbarkeit ohne komplizierten Softwarestack zu erwarten ist. Die konkrete Transformation dieser Inhalte in die hier zu sehende Darstellung erfolgt dabei per [Jupyter Book](https://jupyterbook.org) {cite}`executable_books_community_2021_2561065`.

Diese Vorlage dient somit der Entwicklung von QUADRIGA OERs und zeigt die Möglichkeiten der Jupyter Book Plattform auf. Zudem stellt sie unsere Empfehlungen, wie diese für die Entwicklung Ihrer OER genutzt werden sollten, dar. Gleichzeitig dient sie selbst als OER, welche das Erlernen der Gestaltung und Entwicklung von (QUADIRGA) OERs unterstützt.

```{admonition} Lernziele
:class: lernziele
1. Nach durcharbeiten der OER kennen Sie sich mit dem Technologiestack der QUADRIGA OERS aus und können bei der Arbeit mit der OER auftretende Fehler den jeweiligen Komponenten zuordnen.
2. Nach durcharbeiten der OER können Sie selbst Inhalte in einer QUADRIGA OER anpassen und diese erweitern.
3. Nach durcharbeiten der OER können Sie ausgehend von diesem OER-Template selbst vollkommen neue OERs im Stil der QUADRIGA OERs erstellen.
```
## Aufbau der OER
Die OER startet mit einer Vorstellung der inhaltlichen Struktur sowie des didaktischen Konzepts einer QUADRIGA OER. Dann wird die technische Umsetzung präsentiert, wobei auf die Entwicklungsumgebung und die Formatierungs- und Darstellungsmöglichkeiten besonders eingegagen wird. Dann folgen Inhalte zur Einbettung eines (Self-)Assessments. Inhaltlich schließt die OER mit einem Fazit, auf welches dann noch das Hinterwerk folgt.

```{figure} ./assets/intro/Aufbau_der_OER.svg
---
align: left
width: 100%
---
```

## Nutzung des Templates

Um dieses Template zu Nutzen können Sie entweder die Template-Funktion in GitHub nutzen, oder Sie laden sich den aktuellen Zustand bspw. als `.zip`-Datei herunter und fügen sie einem neuen Repositorium hinzu.

Passen Sie dann die Inhalte an. Insbesondere sollten Sie achten auf die Einstellungen in `_config.yml` und das Inhaltsverzeichnis in `_toc.yml`.

Wollen Sie GitHub-Pages für die Veröffentlichung des Jupyter Books nutzen, so müssen Sie einerseits die Funktionalität in den Einstellungen der Repositoriums anpassen und die GitHub Action in `.github/workflows/deploy-book.yml` anpassen und aktivieren. Zudem muss das Repositorium normalerweise öffentlich sein.

## Inhaltsverzeichnis

```{tableofcontents}
```

# Literatur
```{bibliography}
:filter: docname in docnames
```