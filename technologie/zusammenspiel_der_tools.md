---
lang: de-DE
---
(zusammenspiel_der_tools)=
# Zusammenspiel der Tools

Der Technologie besteht aus verschiedenen Programmen und Dateitypen. Die Inhalte der OER werden in Markdown-Dateien (`.md`) und Jupyter Notebooks (`.ipynb`) verfasst. In diese Dateien können zusätzlich zum reinen Text statische Inhalte wie Abbildungen und dynamische Inhalte wie Programmcode integriert werden.

Die Inhalte werden dann vom Programm `jupyter-book` in eine Website (bestehend aus `.html`-, `.css`- und `.js`-Dateien) übersetzt. Beinhaltet eine Inhaltsdatei Programmcode, so wird dieser ausgeführt und die Programmergebnisse werden entsprechend der Konfiguration in die Inhaltsdatei eingebettet. Dieser Schritt wird einerseits von den Entwickler:innen während des Schreibens lokal durchgeführt, andererseits bei in GitHub veröffentlichten Änderungen automatisch durch eine GitHub Action übernommen.

Die entstandene Website kann anschließend veröffentlicht/gehostet werden. Nutzer:innen könne dazu die Ergebnisse des Programms `jupyter-book` auf einen Web-Server kopieren. Im Falle dieser OER übernimmt auch diesen Schritt die GitHub Action, wobei die Rolle des Webservers durch den kostenlosen Dienst GitHub Pages übernommen wird.

Auf die hier vorgestellten Technologien und deren Zusammenspiel wird im Laufenden jeweils genauer eingegangen. Die Entwicklungsumgebung wird dabei genauer in {numref}`%s Entwicklungsumgebung<entwicklung:einleitung>` vorgestellt. Die Eigenschaften und Fähigkeiten von Markdown-Dateien und Jupyter Notebooks werden genauer in {numref}`%s Entwicklungsumgebung<formatierung:einleitung>` behandelt.


## Jupyter Book vs. Jupyter Notebook

Jupyter Book ist ein Programm, das HTML-Dateien (oder PDFs, …) generiert basierend auf Inhalten und einer Struktur, die Sie erstellen.

Jupyter Notebooks sind ausführbare Dokumente, die statische Elemente wie Text (geschrieben in Markdown) und ausführbare Elemente (also Programmcode) in sogenannten Cells (Zellen) verbinden. Der Programmcode kann in mehreren Programmiersprachen verfasst sein und wird in einem sogenannten Kernel ausgeführt. Wenn Sie eine Zelle ausführen, dann wird der Code in der Zelle an den Kernel übertragen, welcher den Code ausführt und dann das Ergebnis zurücksendet. Das Ergebnis wird dann im Dokument direkt unterhalb der Code-Zelle angezeigt. 

Jupyter Book kann Jupyter Notebooks als Dokumenttyp einlesen und verarbeiten. Während die HTML-Seiten gebaut werden wird das Notebook von Jupyter Book ausgeführt, sodass in den HTML-Seiten auch die Ergebnisse des Codes dargestellt werden.

Jupyter Book basiert auf dem Programm <a href="https://www.sphinx-doc.org/en/master/" class="external-link" target="_blank">Sphinx</a>, welches für die Generierung von Dokumentationen (hauptsächlich im Bereich der Programmierung) entwickelt wurde.