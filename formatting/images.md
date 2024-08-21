# Abbildungen einfügen

Jupyter Book bietet verschiedene Möglichkeiten an, um Abbildungen einzufügen. Für QUADRIGA empfehlen wir Ihnen die Nutzung einer `{figure}`-Umgebung.

Diese Umgebung erlaubt eine Konfiguration bspw. der Breite der Abbildung und integriert eine Bildunterschrift. Wie im Beispiel unten (siehe {numref}`git-branches-development`) kann auch das Attribut `name` definiert werden, welches es erlaubt eine Referenzierung. Neben der Bildunterschrift kann auch eine Textuelle Beschreibung (oft bekannt als Alt-Text) im Attribut `alt` hinterlegt werden, welche bspw. im Screenreader vorgelesen wird.
````
```{figure} ../assets/develop/git/Git_branches_ueber_die_Zeit.svg
---
align: left
width: 100%
name: git-branches-development
alt: Darstellung einer zeitlichen Entwicklung mehrerer Commits und Branches. Ausgehend vom Branch main wird ein Branch tutorial angelegt. In diesem wird ein Commit gespeichert. Dann wird in main ein anderer Commit gespeichert. Im nächsten Schritt wird noch ein Commit im Branch tutorial erzeugt. Am Ende wird der Branch tutorial in den Branch main gemerget.
---
Darstellung einer zeitlichen Entwicklung mehrerer Commits und Branches.
```
````
```{figure} ../assets/develop/git/Git_branches_ueber_die_Zeit.svg
---
align: left
width: 100%
name: git-branches-development
alt: Darstellung einer zeitlichen Entwicklung mehrerer Commits und Branches. Ausgehend vom Branch main wird ein Branch tutorial angelegt. In diesem wird ein Commit gespeichert. Dann wird in main ein anderer Commit gespeichert. Im nächsten Schritt wird noch ein Commit im Branch tutorial erzeugt. Am Ende wird der Branch tutorial in den Branch main gemerget.
---
Darstellung einer zeitlichen Entwicklung mehrerer Commits und Branches.
```
