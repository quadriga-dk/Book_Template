---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
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
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
```

Dann kann das _directive_ `{code-cell}` genutzt werden um einen ausführbaren
Code-Block zu definieren.

```{code-cell}
print(2 + 2)
```
