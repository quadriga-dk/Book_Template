---
lang: de-DE
---

# QUADRIGA OERs: erstellen und gestalten mit Jupyter Book

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
`````{margin}
````{admonition} Zitierhinweis
:class: citation-information
```{literalinclude} /CITATION.bib
:language: bibtex
```
Schnaitter, H., Samoilova, E. & Islam, L. (2024). _QUADRIGA OERs: erstellen und gestalten mit Jupyter Book. QUADRIGA Open Educational Resources: Template._ https://doi.org/10.5281/zenodo.14970672

````
`````

Diese Vorlage dient der Erstellung von Open Educational Resources (OER) im Rahmen des <a href="https://www.quadriga-dk.de/" class="external-link" target="_blank">QUADRIGA-Projekts</a>.


Zur einfachen Erstellung und langfristigen, technikunabhängigen Nutzbarkeit werden QUADRIGA-OERs mit Markdown-Dateien und Jupyter-Notebooks erstellt. Die konkrete Transformation dieser Inhalte in die hier zu sehende Darstellung erfolgt dabei per <a href="https://jupyterbook.org" class="external-link" target="_blank">Jupyter Book</a> {cite}`executable_books_community_2021_2561065`.


Diese Vorlage dient somit der Entwicklung von QUADRIGA OERs und zeigt die Möglichkeiten der Jupyter Book Plattform auf. Zudem stellt sie unsere Empfehlungen, wie diese für die Entwicklung Ihrer OER genutzt werden sollten, dar. Gleichzeitig dient sie selbst als OER, welche das Erlernen der Gestaltung und Entwicklung von (QUADIRGA) OERs unterstützt.

Die QUADRIGA-Vorlagen sind speziell für OERs konzipiert, die auf realen Forschungsbeispielen basieren. Sie wurden so entwickelt, dass sie direkt verwendet und mit eigenen Inhalten gefüllt werden können. Diese Seite des interaktives Lehrbuchs dient als Startseite. Hier sollten Sie eine kurze Beschreibung Ihrer Fallstudie geben und, wenn möglich, ein Bild einfügen, das die Essenz des Inhalts widerspiegelt.

```{figure} /assets/intro/oer-creation-process.png
---
align: center
width: 70%
---
Erstellung von QUADRIGA-OERs aus der Jupyter-Book-Vorlage
```
## Zielgruppe
Die Fallstudie richtet sich an Personen, die ihre Fallstudien unter Verwendung der QUADRIGA-Vorlage erstellen möchten. Einzelne Kapitel können jedoch auch für Lernende von Relevanz sein, beispielsweise hinsichtlich der lokalen Nutzung von Jupyter Books auf eigenen Geräten oder der Anwendung von Google Colab.

## Struktur der Fallstudie
Im QUADRIGA-Projekt entwickeln wir Fallstudien, die auf datengetriebenen Forschungsaktivitäten basieren und spezifische Forschungsfragen zusammen mit den dazugehörigen Datensätzen und Methoden abbilden. Ihre Fallstudie sollte in empirische Schritte unterteilt werden, die:
* dem Datenlebenszyklus folgen,
* den strukturellen Rahmen für Lehrmaterialien bilden,
* den einzelnen Kapiteln im interaktives Lehrbuch entsprechen.

Diese Schritte sollten in diesem Abschnitt visualisiert und kurz beschrieben werden.

```{figure} ./assets/intro/Aufbau_der_OER.svg
---
align: left
width: 100%
---
Flussdiagramm der QUADRIGA-Vorlage, die sich aus sechs Schritten zusammensetzt.
```
In diesem interaktives Lehrbuch durchlaufen wir die folgenden Schritte:

* Im **1. Schritt** führen wir in die OER ein, indem wir die Lernziele definieren und die technischen Voraussetzungen klären (siehe Kapitel {ref}`Präambel<lernziele>`).
* Im **2. Schritt** stellen wir die inhaltliche Struktur einer QUADRIGA OER vor und erläutern das zugrundeliegende didaktische Konzept (siehe Kapitel {ref}`Struktur und didaktisches Konzept<struktur:einleitung>`).
* Im **3. Schritt** beschäftigen wir uns mit der technischen Umsetzung, wobei wir das Zusammenspiel der verschiedenen Tools und deren grafische Aufbereitung betrachten im Detail betrachten. (siehe Kapitel {ref}`Technologie<technologie:einleitung>`).
* Im **4. Schritt** präsentieren wir zuerst allgemeine Hinweise zu Formatierungs und Darstellungsmöglichkeiten und geben dann konkrete Vorgaben und Empfehlungen für QUADRIGA OER (siehe Kapitel {ref}`Formatierung<formatierung:einleitung>`).
* Im **5. Schritt** widmen wir uns der Lernstandskontrolle, indem wir die Rolle des Assessments in QUADRIGA OER erläutern und dessen konkrete Umsetzungsmöglichkeiten aufzeigen (siehe Kapitel {ref}`Lernstandskontrolle (Assessment)<assesssment:einleitung>`).
* Im **6. Schritt** schließen wir die OER inhaltlich mit einem Abschlussassessment ab, fassen die wichtigsten Punkte zusammen und geben weiterführende Hinweise (siehe Kapitel {ref}`Reflexion und Resümee<reflexion>`).

Die OER wird durch den Epilog komplettiert, das Raum für Fragen und Feedback bietet, das Literaturverzeichnis enthält, die Autor:innen vorstellt sowie Informationen zu QUADRIGA und das Impressum bereitstellt (siehe Kapitel {ref}`Epilog<fragen_feedback>`).

## Literatur
```{bibliography}
:filter: docname in docnames
:style: plain
```