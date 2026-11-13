# Nützliche Dokumentation(en) und Links

## Markdown

- <a href="https://jupyterbook.org/v1/reference/cheatsheet.html" class="external-link" target="_blank">Markdown Cheatsheet für Jupyter Book</a>
- <a href="https://jupyterbook.org/v1/content/citations.html" class="external-link" target="_blank">Zitationen in Jupyter Book</a>
  - <a href="https://jupyterbook.org/v1/content/citations.html#citing-a-work-in-different-documents" class="external-link" target="_blank">Abschnitt zur Zitation eines Werks in mehreren Dokumenten</a>
- <a href="https://jupyterbook.org/v1/content/figures.html" class="external-link" target="_blank">Abbildungen in Jupyter Book</a>

### Videos als Abbildungen

`{figure}` kann neben Bilddateien auch Videos (`.mp4`, `.webm`, `.ogv`) einbinden. Die lokale Sphinx-Erweiterung `_ext/video_figure.py` (registriert in `_config.yml` unter `sphinx.local_extensions`) rendert dafür ein `<video>`-Element statt eines `<img>`; Bildunterschrift, Nummerierung ("Fig. X.Y") und Querverweise bleiben unverändert. Die Videodateien werden beim Build nach `_videos/` kopiert.

Die Videos laufen stumm in einer Schleife und haben keine eingeblendeten Bedienelemente (wie die früheren GIFs). Ein Klick auf das Video – oder `Leertaste`/`Enter`, wenn es den Fokus hat – hält die Animation an und startet sie wieder; außerhalb des sichtbaren Bereichs pausieren die Videos automatisch (`_static/video-figure.js`).

````markdown
```{figure} ../assets/beispiel.mp4
---
align: center
width: 100%
name: beispiel-animation
alt: Beschreibung der Animation für Screenreader.
---
Bildunterschrift der Animation.
```
````

Bitte keine animierten GIFs mehr einbinden: Videos sind bei gleicher Qualität rund 20-mal kleiner und halten den Pages-Deploy schnell. Erzeugen lässt sich ein MP4 aus einem GIF zum Beispiel mit:

```bash
ffmpeg -i eingabe.gif -an -c:v libx264 -preset slow -crf 23 \
  -pix_fmt yuv420p -movflags +faststart ausgabe.mp4
```



## Git

- <a href="https://git-scm.com/docs/git" class="external-link" target="_blank">Git Dokumentation</a>
- <a href="https://wizardzines.com/git-cheat-sheet.pdf" class="external-link" target="_blank">Julia Evans – Git Cheat-Sheet</a> (PDF)
- <a href="https://www.git-scm.com/book/en/v2" class="external-link" target="_blank">Scott Chacon & Ben Straub – Pro Git</a> (Website, PDF, EPUB)


## Über `requirements.txt` installierte Pakete upgraden

Sollen Pakete auf die aktuellste Version gebracht werden, auch wenn dies den Vorgaben in `requirements.txt` widerspricht, so können einzelne Pakete wie folgt aktualisiert werden:

```bash
(venv)$ pip install -U jupyter-book
```

Sollen alle Pakete aktualisiert werden, geht dies mit dem nachfolgenden Befehl:

```bash
(venv)$ cat requirements.txt | cut -f1 -d= | xargs pip install -U
```

Nachdem ein Paket aktualisiert wurde, sollte die Funktionalität überprüft werden. Funktioniert alles weiterhin, so kann der neue Stand der installierten Versionen wieder in der `requirements.txt` gesichert werden:

```bash
(venv)$ pip freeze > requirements.txt
```
