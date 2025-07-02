---
lang: de-DE
---

(jupyter_kernel)=
# Jupyter Kernels

Jupyter Kernels sind die Recheneinheiten, die Code in Jupyter Notebooks ausführen. Wenn Sie ein Jupyter Book mit ausführbarem Inhalt oder Code erstellen, ist das Verständnis von Kernels sowohl für die lokale Entwicklung als auch für automatisierte Builds von entscheidender Bedeutung.

```{admonition} Was ist ein Jupyter Kernel?
:class: hinweis

Ein Jupyter Kernel ist ein separater Prozess, der Ihren Code ausführt und mit der Jupyter-Benutzeroberfläche kommuniziert. Wenn Sie Code in Ihrem Buch schreiben, nimmt der Kernel Ihren Code entgegen, führt ihn in der entsprechenden Programmiersprache aus und liefert die Ergebnisse zurück.
```

## Grundlagen und Funktionsweise

Jupyter Notebooks können mit vielen verschiedenen Programmiersprachen arbeiten – Python, R, Julia, Scala und sogar spezialisierte Sprachen wie SPARQL für Datenbankabfragen. Jede Sprache benötigt ihre eigene Ausführungsumgebung, um den Code korrekt zu verarbeiten. Deshalb brauchen wir verschiedene Kernels für verschiedene Sprachen.

Ohne Kernels:
- Würde Ihr Code nicht ausgeführt
- Würden Variablen nicht zwischen Zellen gespeichert
- Könnten Sie keine Ausgaben, Diagramme oder Ergebnisse sehen

Die am häufigsten verwendeten Kernels in Jupyter Books sind der **IPython Kernel** für Python-Code, der **IR Kernel** für R-Code und der **SPARQL Kernel** für Datenbankabfragen mit der SPARQL-Abfragesprache zur Arbeit mit Wissensgraphen und semantischen Daten.

## Kernels in GitHub Actions einrichten

Wenn Sie Ihr Jupyter Book lokal erstellen, sind die Kernels bereits auf Ihrem Computer installiert. GitHub Actions startet jedoch mit einer sauberen Umgebung, sodass Sie die Kernels dort erst installieren und konfigurieren müssen.

### Python Kernel

Die Python-Einrichtung ist unkompliziert, da Python den IPython Kernel mitbringt:

```yaml
- name: Set up Python 3.11
  uses: actions/setup-python@v5
  with:
    python-version: 3.11
    cache: pip  # Pip-Abhängigkeiten zwischenspeichern für schnellere Builds

- name: Install Python dependencies
  run: |
    pip install -r requirements.txt
```

### R Kernel

R erfordert mehr Schritte, da wir sowohl R als auch den IRkernel installieren müssen:

```yaml
- name: Set up R
  uses: r-lib/actions/setup-r@v2

- name: Install R dependencies
  uses: r-lib/actions/setup-r-dependencies@v2
  with:
    cache: true              # R-Pakete zwischenspeichern für schnellere Builds
    cache-version: 2         # Cache-Version (bei Bedarf aktualisieren)
    packages: |              # Liste der zu installierenden R-Pakete
      any::tidyverse         # Datenmanipulation und -visualisierung
      any::IRkernel          # Der eigentliche R-Kernel für Jupyter
    install-pandoc: false    # Pandoc überspringen (nicht für Jupyter Book benötigt)
    install-quarto: false    # Quarto überspringen (nicht für Jupyter Book benötigt)

- name: Set up IRkernel
  run: |
    IRkernel::installspec(name="ir", displayname="R")
  shell: Rscript {0}         # Als R-Skript ausführen
```

### SPARQL Kernel einrichten

Die SPARQL Kernel-Installation ist einfach, sobald Python eingerichtet ist:

```yaml
- name: Install SPARQL Kernel
  run: |
    jupyter sparqlkernel install --user  # SPARQL Kernel für aktuellen Benutzer installieren
```

### Mehrere Kernels kombinieren

Möchten Sie in einem Workflow mehrere Programmiersprachen unterstützen, so fügen Sie alle Einrichtungsschritte nacheinander ein. Entscheidend ist, dass sämtliche Kernel installiert sind, bevor der Build des Books gestartet wird.

### Kernels überprüfen

Es ist immer eine gute Praxis zu überprüfen, ob alle Ihre Kernels ordnungsgemäß installiert sind:

```yaml
- name: Log all available kernels
  run: |
    jupyter kernelspec list
```

Dieser Befehl zeigt Ihnen alle Kernels an, die GitHub Actions zur Ausführung Ihrer Notebooks verwenden kann.

Das Verständnis von Kernels hilft Ihnen bei der Fehlerbehebung, wenn Notebooks nicht ordnungsgemäß ausgeführt werden, und stellt sicher, dass Ihr Jupyter Book sowohl lokal als auch in automatisierten Umgebungen erfolgreich erstellt wird.


```{admonition} Zusätzliche Materialien
:class: seealso

Für detailliertere Informationen über Jupyter Kernels schauen Sie sich diese Ressourcen an:
- <a href="https://docs.jupyter.org/en/stable/projects/kernels.html" class="external-link" target="_blank">Offizielle Jupyter Kernels Dokumentation</a> 
- <a href="https://docs.jupyter.org/en/latest/install/kernels.html" class="external-link" target="_blank">Installation von Kernels</a> 
- <a href="https://jupyter-client.readthedocs.io/en/latest/kernels.html" class="external-link" target="_blank">Entwicklung eigener Kernels für Jupyter</a> 
- <a href="https://github.com/jupyter/jupyter/wiki/Jupyter-kernels" class="external-link" target="_blank">Liste verfügbarer Jupyter Kernels</a>

```