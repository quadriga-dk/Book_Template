---
lang: de-DE
---

(formatierung:admonitions)=
# Admonitions

Sogenannte Admonitions werden genutzt, um bestimmte Inhalte hervorzuheben. In QUADRIGA OER nutzen wir dafür die folgenden Typen.


`````{admonition} Übung
:class: exercise
Um Übungen kennzuzeichnen wird dieser Admonition-Typ genutzt.
````
```{admonition} Übung
:class: exercise
Um Übungen kennzuzeichnen wird dieser Admonition-Typ genutzt.
```
````
`````


`````{admonition}  Lösungen
:class: solution, dropdown
Lösungen werden mit diesem Admonition-Typ gekennzeichnet. Sie können ggf. auch innerhalb einer Übungs-Admonition dargestellt werden.
````
```{admonition}  Lösungen
:class: solution, dropdown
Lösungen werden mit diesem Admonition-Typ gekennzeichnet. Sie können ggf. auch innerhalb einer Übungs-Admonition dargestellt werden.
```
````
`````

`````{admonition} Lernziele
:class: lernziele
Lernziele werden mit diesem Admonition-Typ gekennzeichnet.
````
```{admonition} Lernziele
:class: lernziele
Lernziele werden mit diesem Admonition-Typ gekennzeichnet.
```
````
`````

`````{admonition} Hinweis
:class: hinweis, dropdown
Hinweise werden mit diesem Admonition-Typ gekennzeichnet. 
````
```{admonition} Hinweis
:class: hinweis, dropdown
Hinweise 
```
````
`````

`````{admonition} Keypoints
:class: keypoint
Wichtige Erkenntnisse, Lernergebnisse und sonstige Keypoints werden mit diesem Admonition-Typ gekennzeichnet.
````
```{admonition} Keypoints
:class: keypoint
Wichtige Erkenntnisse, Lernergebnisse und sonstige Keypoints werden mit diesem Admonition-Typ gekennzeichnet.
```
````
`````

`````{admonition} Achtung
:class: caution
Ist bei einem Arbeitsschritt besondere Vorsicht geboten, um bspw. Dateiverlust zu vermeiden, so wird dieser Admonition-Typ genutzt.
````
```{admonition} Achtung
:class: caution
Ist bei einem Arbeitsschritt besondere Vorsicht geboten, so wird dieser Admonition-Typ genutzt.
```
````
`````

`````{admonition} Weiterführende Literatur / zusätzliche Materialien
:class: seealso
Weiterführende Literaturhinweise oder zusätzliche (externe) Materialien werden so gekennzeichnet.

Verweise können hierbei auf andere Bestandteile der OER, andere QUADRIGA OER oder auch Inhalte dritter zeigen. Links sollten dabei immer in einem neuen Tab öffnen und falls sie auf externe Seiten verweisen mit der CSS-Klasse `.external-link` markiert werden.
````html
<a href="https://example.com" class="external-link" target="_blank">Linktext</a>
````
````
```{admonition} Weiterführende Literatur / zusätzliche Materialien
:class: seealso
Weiterführende Literaturhinweise oder zusätzliche (externe) Materialien werden so gekennzeichnet.
```
````
`````

`````{admonition} Bearbeitungszeit
:class: zeitinfo
Dieser Admonition-Typ wird verwendet, um die voraussichtliche Bearbeitungszeit für Aufgaben oder Kapitel anzugeben.
````
```{admonition} Bearbeitungszeit/Zeitinfo
:class: zeitinfo
Informiert Lernende über den voraussichtlichen Zeitaufwand für Abschnitte oder Aufgaben.
```
````
`````

``````{admonition} Zitierhinweis
:class: citation-information
```{literalinclude} ../CITATION.bib
:language: bibtex

```
```bibtex
@incollection{schnaitter_technologie_2024,
    address = {Potsdam; Berlin},
    title = {Technologie},
    copyright = {CC-BY-SA 4.0},
    url = {https://quadriga-dk.github.io/Book_Template/technologie/einführung.html},
    language = {deu},
    booktitle = {{QUADRIGA} {OERs}: erstellen und gestalten mit {Jupyter Book}. {QUADRIGA} {Open} {Educational} {Ressources}: {Template}.},
    author = {Schnaitter, Hannes and Samoilova, Evgenia and Islam, Lamia},
    year = {2024},
}
```
Schnaitter, H., Samoilova, E. & Islam, L. (2024). Technologie In _QUADRIGA OERs: erstellen und gestalten mit Jupyter Book. QUADRIGA Open Educational Resources: Template._ https://quadriga-dk.github.io/Book_Template/technologie/einführung.html

`````
````{admonition} Zitierhinweis
:class: citation-information
```{literalinclude} ../CITATION.bib
:language: bibtex

```
Schnaitter, H., Samoilova, E. & Islam, L. (2024). _QUADRIGA OERs: erstellen und gestalten mit Jupyter Book. QUADRIGA Open Educational Resources: Template._ https://doi.org/10.5281/zenodo.14970672
````
`````
``````