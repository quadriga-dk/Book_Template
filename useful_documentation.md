---
lang: de-DE
---
# Nützliche Dokumentation(en) und Links

## Markdown

- <a href="https://jupyterbook.org/en/stable/reference/cheatsheet.html" class="external-link" target="_blank">Markdown Cheatsheet für Jupyter Book</a>
- <a href="https://jupyterbook.org/en/stable/content/citations.html" class="external-link" target="_blank">Zitationen in Jupyter Book</a>
  - <a href="https://jupyterbook.org/en/stable/content/citations.html#citing-a-work-in-different-documents" class="external-link" target="_blank">Abschnitt zur Zitation eines Werks in mehreren Dokumenten</a>
- <a href="https://jupyterbook.org/en/stable/content/figures.html" class="external-link" target="_blank">Abbildungen in Jupyter Book</a>


## Git

- <a href="https://git-scm.com/docs/git" class="external-link" target="_blank">Git Dokumentation</a>
- <a href="https://wizardzines.com/git-cheat-sheet.pdf" class="external-link" target="_blank">Julia Evans – Git Cheat-Sheet</a> (PDF)
- <a href="https://www.git-scm.com/book/en/v2" class="external-link" target="_blank">Scott Chacon & Ben Straub – Pro Git</a> (Website, PDF, EPUB)


## über `requirements.txt` installierte Pakete upgraden

Sollen Pakete auf die aktuellste Version gebracht werden, auch wenn dies den Vorgaben in `requirements.txt` widerspricht, so können einzelne Pakete wie folgt aktualisiert werden:

```bash
(venv)$ pip install -U jupyter-book
```

Sollen alle Pakete aktualisiert werden geht dies mit den nachfolgenden Befehl:

```bash
(venv)$ cat requirements.txt | cut -f1 -d= | xargs pip install -U
```

Nachdem ein Paket aktualisiert wurde sollte die Funktionalität überprüft werden. Funktioniert alles weiterhin, so kann der neue Stand der installierten Versionen wieder in der `requirements.txt` gesichert werden:

```bash
(venv)$ pip freeze > requirements.txt
```