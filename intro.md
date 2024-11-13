# Ihre QUADRIGA OER

Diese Vorlage dient der Entwicklung von QUADRIGA OERs. Sie zeigt die Möglichkeiten der Jupyter Book Platform und unsere Empfehlungen, wie sie für die Entwicklung Ihrer OER genutzt werden sollten.

Wenn Sie mehr zu Jupyter Book {cite}`executable_books_community_2021_2561065` erfahren wollen, nutzen die [Dokumentation von Juypter Book](https://jupyterbook.org).

## Jupyter Book vs. Jupyter Notebook

Jupyter Book ist ein Programm, das HTML-Dateien (oder PDFs, …) generiert basierend auf Inhalten und einer Struktur, die Sie erstellen.

Jupyter Notebooks sind ausführbare Dokumente, die statische Elemente wie Text (geschrieben in Markdown) und ausführbare Elemente (also Programmcode) in sogenannten Cells (Zellen) verbinden. Der Programmcode kann in mehreren Programmiersprachen verfasst sein und wird in einem sogenannten Kernel ausgeführt. Wenn Sie eine Zelle ausführen, dann wird der Code in der Zelle an den Kernel übertragen, welcher den Code ausführt und dann das Ergebnis zurücksendet. Das Ergebnis wird dann im Dokument direkt unterhalb der Code-Zelle angezeigt. 

Jupyter Book kann Jupyter Notebooks als Dokumenttyp einlesen und verarbeiten. Während die HTML-Seiten gebaut werden wird das Notebook von Jupyter Book ausgeführt, sodass in den HTML-Seiten auch die Ergebnisse des Codes dargestellt werden.

Jupyter Book basiert auf dem Programm [Sphinx](https://www.sphinx-doc.org/en/master/), welches für die Generierung von Dokumentationen (hauptsächlich im Bereich der Programmierung) entwickelt wurde.

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