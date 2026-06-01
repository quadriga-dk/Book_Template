# H5P-Einbindung

H5P-Aktivitaeten koennen in dieser Jupyter Book-Vorlage als statische Inhalte
ueber GitHub Pages bereitgestellt werden. Die Aktivitaet wird dabei als kleine
Standalone-HTML-Seite unter `_static/h5p/` abgelegt und anschliessend per
`iframe` in eine Buchseite eingebunden.

## Ordnerstruktur

Legen Sie pro Aktivitaet einen eigenen Ordner an:

```text
_static/
  h5p/
    my-activity/
      index.html
      content/
      dist/
```

Die Datei `index.html` kann aus `_static/h5p/_template/index.html` kopiert
werden. In `content/` liegt der entpackte Inhalt der `.h5p`-Datei; in `dist/`
liegen die Dateien aus `h5p-standalone`.

## Einbettung

Auf einer Seite innerhalb eines Unterordners, zum Beispiel in
`inhaltskapitel/`, wird die Aktivitaet so eingebunden:

```html
<iframe
  src="../_static/h5p/my-activity/index.html"
  title="H5P activity"
  width="100%"
  height="650"
  style="border: 0;"
  loading="lazy"
  allowfullscreen>
</iframe>
```

Auf einer Seite im Wurzelverzeichnis der OER verwenden Sie stattdessen:

```html
<iframe
  src="_static/h5p/my-activity/index.html"
  title="H5P activity"
  width="100%"
  height="650"
  style="border: 0;"
  loading="lazy"
  allowfullscreen>
</iframe>
```

GitHub Pages stellt die Aktivitaet nach dem Build unter folgendem Muster bereit:

```text
https://quadriga-dk.github.io/Book_Template/_static/h5p/my-activity/index.html
```

```{admonition} Hinweis
:class: hinweis
Diese statische Einbindung zeigt H5P-Inhalte an, speichert aber keine
Ergebnisse, Versuche oder Punktzahlen. Fuer Tracking ist eine LMS-Integration
oder ein Dienst wie H5P.com erforderlich.
```
