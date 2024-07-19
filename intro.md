# Ihre QUADRIGA OER

Diese Vorlage dient der Entwicklung von QUADRIGA OERs. Sie zeigt die Möglichkeiten der Jupyter Book Platform und unsere Empfehlungen, wie sie für die Entwicklung Ihrer OER genutzt werden sollten.

Wenn Sie mehr zu Jupyter Book erfahren wollen, nutzen die [Dokumentation von Juypter Book](https://jupyterbook.org).

## Jupyter Book vs. Jupyter Notebook

Jupyter Book ist ein Programm, das HTML-Dateien (oder PDFs, …) generiert basierend auf Inhalten und einer Struktur, die Sie erstellen.

Jupyter Notebooks sind ausführbare Dokumente, die statische Elemente wie Text (geschrieben in Markdown) und ausführbare Elemente (also Programmcode) in sogenannten Cells (Zellen) verbinden. Der Programmcode kann in mehreren Programmiersprachen verfasst sein und wird in einem sogenannten Kernel ausgeführt. Wenn Sie eine Zelle ausführen, dann wird der Code in der Zelle an den Kernel übertragen, welcher den Code ausführt und dann das Ergebnis zurücksendet. Das Ergebnis wird dann im Dokument direkt unterhalb der Code-Zelle angezeigt. 

Jupyter Book kann Jupyter Notebooks als Dokumenttyp einlesen und verarbeiten. Während die HTML-Seiten gebaut werden wird das Notebook von Jupyter Book ausgeführt, sodass in den HTML-Seiten auch die Ergebnisse des Codes dargestellt werden.

Jupyter Book basiert auf dem Programm [Sphinx](https://www.sphinx-doc.org/en/master/), welches für die Generierung von Dokumentationen (hauptsächlich im Bereich der Programmierung) entwickelt wurde.

## Nutzung des Templates

## Inhaltsverzeichnis

```{tableofcontents}
```

# old english parts

## How to use this Template
A Jupyter Book consists of a configuration file (`_config.yml`), a table of contents (`_toc.yml`) and at least one content file in the formats Markdown, MyST or Jupyter Notebook.  Markdown files are always treated as MyST even, if you don't use any of its special features.

To create a new QUADRIGA OER you can fork this repository and make your changes. Or you can simply create a new repository and then copy the files of this repository.


