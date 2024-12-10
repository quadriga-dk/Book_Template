---
lang: de-DE
---

# QUADRIGA OERs: erstellen und gestalten mit Jupyter Book

```{sidebar} <i class="fas fa-question-circle icon"></i> Ask a Data Steward

Haben Sie Fragen oder Feedback? <br>
<a href="https://github.com/quadriga-dk/Book_Template/issues/new" class="external-link" target="_blank">
    Erstellen Sie ein Issue
</a> auf GitHub, um Hilfe von unseren Datenverwaltern zu erhalten!

Wir schätzen Ihr Feedback und werden so schnell wie möglich antworten.
```

Diese Vorlage dient der Erstellung von Open Educational Resources (OER) im Rahmen des <a href="https://www.quadriga-dk.de/" class="external-link" target="_blank">QUADRIGA-Projekts</a>.


Zur einfachen Erstellung und langfristigen, technikunabhängigen Nutzbarkeit werden QUADRIGA-OERs mit Markdown-Dateien und Jupyter-Notebooks erstellt. Die konkrete Transformation dieser Inhalte in die hier zu sehende Darstellung erfolgt dabei per <a href="https://jupyterbook.org" class="external-link" target="_blank">Jupyter Book</a> {cite}`executable_books_community_2021_2561065`.


Diese Vorlage dient somit der Entwicklung von QUADRIGA OERs und zeigt die Möglichkeiten der Jupyter Book Plattform auf. Zudem stellt sie unsere Empfehlungen, wie diese für die Entwicklung Ihrer OER genutzt werden sollten, dar. Gleichzeitig dient sie selbst als OER, welche das Erlernen der Gestaltung und Entwicklung von (QUADIRGA) OERs unterstützt.

Die QUADRIGA-Vorlagen sind speziell für OERs konzipiert, die auf realen Forschungsbeispielen basieren. Sie wurden so entwickelt, dass sie direkt verwendet und mit eigenen Inhalten gefüllt werden können. Diese Seite des Jupyter Books dient als Startseite. Hier sollten Sie eine kurze Beschreibung Ihrer Fallstudie geben und, wenn möglich, ein Bild einfügen, das die Essenz des Inhalts widerspiegelt.

```{figure} /assets/intro/oer-creation-process.png
---
align: center
width: 70%
---
Erstellung von QUADRIGA-OERs aus der Jupyter-Book-Vorlage
```
## Aufbau der OER
Die OER startet mit einer Vorstellung der inhaltlichen Struktur sowie des didaktischen Konzepts einer QUADRIGA OER. Dann wird die technische Umsetzung präsentiert, wobei auf die Entwicklungsumgebung und die Formatierungs- und Darstellungsmöglichkeiten besonders eingegagen wird. Dann folgen Inhalte zur Auswahl und Einbettung eines (Self-)Assessments. Inhaltlich schließt die OER mit einem Fazit, auf welches noch das Hinterwerk folgt.

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

## Literatur
```{bibliography}
:filter: docname in docnames
```