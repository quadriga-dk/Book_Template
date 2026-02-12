---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.1
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
---

(formatierung:myst_notebooks)=

# MyST-Markdown basierte Notebooks

Markdown-Dateien in MyST können um Metadaten (sog. frontmatter) erweitert
werden, wodurch sie wie Jupyter Notebooks ausführbare Inhalte beinhalten
können.

Dafür muss die Markdown-Datei mit der folgenden frontmatter (für ein Python
Notebook) beginnen:

```
---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.1
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
---
```

Dann kann das _directive_ `{code-cell}` genutzt werden um einen ausführbaren
Code-Block zu definieren.

```{code-cell} ipython3
print(2 + 2)
```

Gegenüber Jupyter Notebooks haben MyST-Markdown-Notebooks den Vorteil, dass
kleine Änderungen auch in Git zu kleinen Diffs führen. Sie sind jedoch nicht so
universell verbreitet. Bspw. müssen in einem JupyterHub extra Programmpakete
installiert werden, damit die Nutzung korrekt funktioniert.
