---
lang: de-DE
---
(gh_page)=
# Jupyter Book mit GitHub Pages veröffentlichen

GitHub Pages ist ein Hosting-Dienst, mit dem digitale Inhalte direkt aus einem GitHub-Repository veröffentlicht werden können. Dadurch können Jupyter Books online bereitgestellt und öffentlich zugänglich gemacht werden. In diesem Abschnitt werden die beiden gängigsten Methoden zur Bereitstellung eines Jupyter Books vorgestellt: 

- Deploy from a branch
- GitHub Actions

```{admonition} Hinweis
:class: hinweis
Damit diese Methoden funktionieren, muss das GitHub-Repository **public** sein.
```

## Deploy from a branch

**Charakteristika:**

- **Funktionsweise:** Manuelles Erstellen und Hochladen der gebauten Dateien auf einen separaten Branch, typischerweise `gh-pages`.
- **Nutzung:** Geeignet für einfache Projekte mit seltenen Änderungen.
- **Vorteil:** Schnell und unkompliziert einzurichten.
- **Einschränkungen:** Erfordert manuelle Schritte bei jedem Update.

**Schritte zur Einrichtung:**

1. **Buch bauen:**  
   ```bash
   jupyter-book build .
   ```
2. **Branch `gh-pages` erstellen:**  
   ```bash
   git checkout -b gh-pages
   ```
3. **Dateien hochladen:**  
   Kopieren Sie die Dateien aus `_build/html` in das Root-Verzeichnis des Branches `gh-pages` und pushen Sie die Änderungen.  
4. **Einstellungen anpassen:**  
   Navigieren Sie zu **Settings > Pages** und wählen Sie bei "Build and Deployment" den Branch `gh-pages` sowie "Root" als Verzeichnis.


## GitHub Actions (Empfohlen)

**Charakteristika:**

- **Funktionsweise:** Automatisiertes Erstellen und Bereitstellen durch definierte Workflows in GitHub Actions.
- **Nutzung:** Optimal für Projekte mit häufigen Änderungen.
- **Vorteil:** Automatisierung reduziert Fehler und spart Zeit.
- **Einschränkungen:** Initialer Aufwand für die Einrichtung der Workflows.

**Schritte zur Einrichtung:**

1. Verzeichnis `.github/workflows/` im Repository erstellen.  
2. Eine Workflow-Datei hinzufügen, z.B.:  

```yaml
name: Deploy Jupyter Book

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install jupyter-book

      - name: Build Jupyter Book
        run: jupyter-book build mybook/

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: mybook/_build/html
```

```{dropdown} Erklärung der Workflow-Datei
- **`name:`** Der Name des Workflows.
- **`on:`** Auslöser für den Workflow (z. B. push auf den Main-Branch). 
- **`jobs:`** Aufgaben, die im Workflow ausgeführt werden.  
- **`runs-on:`** Gibt die Umgebung für den Workflow an (z. B. `ubuntu-latest`).  
- **`steps:`** Einzelne Schritte innerhalb des Jobs:
    - **Checkout code:** Mit `actions/checkout` wird der Code des Repositories geladen.
    - **Set up Python:** Nutzt `actions/setup-python`, um die gewünschte Python-Version einzurichten.
    - **Install dependencies:** Benötigte Pakete, wie Jupyter Book, werden installiert.
    - **Build Jupyter Book:** Das Buch wird erstellt.
    - **Deploy to GitHub Pages:** Das fertige HTML wird hochgeladen.
```

## Vergleich der Methoden

| Methode               | Vorteile                           | Nachteile                             |
|-----------------------|------------------------------------|---------------------------------------|
| Deploy from a branch  | Einfache Einrichtung               | Manuelle Updates                      |
| GitHub Actions        | Automatisch, konsistent, flexibel  | Erfordert initiale Einrichtung        |

## Zugriff auf das veröffentlichte Buch

Die publizierte Version Ihres Jupyter Books ist verfügbar unter:  
`https://<username>.github.io/<repository-name>`


## Zusammenfassung

Die Wahl der Bereitstellungsmethode hängt von den Anforderungen Ihres Projekts ab. Während die Branch-Bereitstellung für einfache Projekte geeignet ist, bietet GitHub Actions mehr Automatisierung und Flexibilität für komplexere oder häufig aktualisierte Inhalte.