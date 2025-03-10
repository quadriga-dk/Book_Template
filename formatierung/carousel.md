---
lang: de-DE
---

(formatierung:Carousel)=
# Carousel

```{admonition} Was ist ein Carousel?
:class: Keypoint
Ein Carousel ist ein interaktives Element, das mehrere Inhalte (wie Bilder, Text oder andere Medien) in einem rotierenden Format anzeigt. Es ermöglicht die platzsparende Präsentation mehrerer Elemente, wobei Benutzer durch die Inhalte navigieren können.
```


````{card-carousel} 1

```{card}
:class-card: carousel-card
![image1](../assets/slides/1.jpg)
```

```{card}
:class-card: carousel-card
![image2](../assets/slides/2.jpg)
```

```{card}
:class-card: carousel-card
![image3](../assets/slides/3.jpg)
```

````

## Anleitung zur Nutzung des benutzerdefinierten Carousels

Diese Beispielseite verwendet ein **angepasstes Carousel**, das mit einer eigenen CSS- und JavaScript-Datei (`carousel.css` und `carousel.js`) ausgestattet ist. Damit das Carousel korrekt funktioniert, müssen diese Dateien in das Jupyter Book eingebunden werden.

### Szenario 1: Dateien sind bereits vorhanden

Falls Sie die `carousel.css` und `carousel.js` Dateien bereits in Ihrem `_static` Ordner haben, können Sie direkt die folgende Syntax verwenden, um das Carousel in Ihrem Jupyter Book zu nutzen:

`````
````{card-carousel} 1

```{card}
:class-card: carousel-card
![Folie1](Bildpfad)
```

```{card}
:class-card: carousel-card
![Folie2](Bildpfad)
```

```{card}
:class-card: carousel-card
![Folie3](Bildpfad)
```

````
`````
### Szenario 2: Dateien sind nicht vorhanden
Falls Sie die `carousel.css` und `carousel.js` Dateien noch nicht haben, folgen Sie diesen Schritten:

#### Dateien herunterladen
Laden Sie die `carousel.css` und `carousel.js` Dateien herunter und speichern Sie sie in Ihrem Projekt.

- [carousel.css](../_static/carousel.css)
- [carousel.js](../_static/carousel.js)


#### Platzierung der Dateien
Die CSS- und JS-Dateien sollten idealerweise in den Ordner `_static` innerhalb Ihres Jupyter Book-Projekts gelegt werden:

```
📂 mein-jupyter-book/
 ┣ 📂 _static/
 ┃ ┣ 📄 carousel.css
 ┃ ┣ 📄 carousel.js
 ┃ ┗ 📄 quadriga.css (falls vorhanden)
 ┣ 📄 _config.yml
 ┣ 📂 content/
 ┗ ...
```

Falls Sie bereits einen anderen Ordner für statische Dateien verwenden, können Sie die Dateien dort ablegen. Der Standardansatz ist jedoch die Verwendung von `_static`.

#### Einbinden der Dateien in `_config.yml`
Um sicherzustellen, dass Sphinx die Dateien lädt, fügen Sie folgende Zeilen in Ihre `config.yml`-Datei ein:

```yaml
sphinx:
  config:
    html_static_path: ['_static']
    html_css_files:
      - quadriga.css  # Falls bereits vorhanden
      - carousel.css
    html_js_files:
      - carousel.js
```

#### Verwendung des Carousels
Nach erfolgreicher Einrichtung können Sie nun das Carousel wie im Szenario 1 beschrieben in Ihrem Jupyter Book verwenden.


