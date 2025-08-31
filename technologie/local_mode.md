# Lokale Ausführung des Jupyter Books

Die Ausführung des Buchs in der lokalen Umgebung bietet Ihnen maximale Kontrolle: Sie können offline arbeiten, auf alle Dateien zugreifen, Ihre eigenen Daten integrieren und das Material frei anpassen. Dies erfordert jedoch die Einrichtung der korrekten Umgebung (Python, R oder SPARQL je nach Kapitel).

 ````{admonition} Hinweis
:class: hinweis
Bevor Sie beginnen, stellen Sie bitte sicher, dass Python auf Ihrem Computer installiert ist. Falls Python fehlt oder veraltet ist, folgen Sie bitte der Installationsanleitung [hier](python).
 ````

## Repository herunterladen

Sie benötigen die Notebooks und Ressourcen aus dem Buch-Repository. Es gibt zwei Möglichkeiten, diese zu erhalten:

1. **Download als ZIP**
    - Gehen Sie zum GitHub-Repository dieses Buchs (rechts oben → GitHub-Symbol).
    - Wählen Sie Code → Download ZIP.
    - Entpacken Sie die ZIP-Datei auf Ihrem Computer.

2. **Oder über Git clone** (falls Sie Git bereits installiert haben)

## Lokale Umgebung erstellen

Im heruntergeladenen Ordner sollten Sie eine lokale Umgebung mit allen benötigten Abhängigkeiten einrichten (siehe `requirements.txt`). Nur so ist sichergestellt, dass die Notebooks korrekt laufen.

Weitere Informationen finden Sie im Abschnitt [Einrichtung der lokalen Entwicklungsumgebung](jupyter_book) für schrittweise Anweisungen, und Sie haben die lokale Version des Jupyter Books bereit!

## Jupyter Notebooks ausführen

Um die Jupyter Notebooks (.ipynb-Dateien) zu öffnen und auszuführen, navigieren Sie in den Buchordner und starten Jupyter über das Terminal:

```bash
jupyter lab
```
oder

```bash
jupyter notebook
```

Dies startet einen lokalen Server und öffnet ein Browserfenster, in dem Sie die Notebooks ausführen oder bearbeiten können.

Um den Server zu stoppen, kehren Sie zum Terminal zurück, in dem er läuft, und drücken `Strg + C`.

## Spezialfälle (andere Programmiersprachen)

Einige Kapitel verwenden möglicherweise `R` oder `SPARQL`. In diesem Fall müssen Sie zusätzliche Kernel installieren.

### R

1. Installieren Sie <a href="https://cran.r-project.org/" target="_blank" class="external-link">R</a> und <a href="https://posit.co/download/rstudio-desktop/" target="_blank" class="external-link">RStudio</a>.
2. Installieren Sie aus R oder RStudio heraus das IRkernel-Paket:
   ```r
   install.packages("IRkernel")
   IRkernel::installspec(user = FALSE)
   ```

Dies registriert R als Jupyter-Kernel, sodass Sie R-Notebooks innerhalb von JupyterLab oder Jupyter Notebook ausführen können.

### SPARQL

Um SPARQL-Abfragen in Jupyter auszuführen, benötigen Sie den SPARQL-Kernel.

1. Stellen Sie sicher, dass Jupyter installiert ist.
2. Installieren Sie den Kernel mit:
   ```bash
   jupyter sparqlkernel install --user
   ```

Danach können Sie SPARQL als Kernel auswählen, wenn Sie relevante Notebooks öffnen.

Wenn Sie mehr über Kernel erfahren möchten, lesen Sie den Abschnitt [Jupyter Kernels](jupyter_kernel).

## Alternative: Einzelnes Notebook herunterladen

Wenn Sie nur ein Kapitel ausprobieren möchten, ohne das vollständige Repository einzurichten:

1. Laden Sie die .ipynb-Datei direkt aus dem Buch herunter (rechts oben → Download-Symbol).
2. Öffnen Sie sie in JupyterLab, Jupyter Notebook oder RStudio.

````{admonition} Achtung!
:class: caution
Möglicherweise benötigen Sie zugehörige Datensätze oder Unterstützungsdateien – diese Einrichtung funktioniert am besten nur für eigenständige, in sich geschlossene Notebooks.
````

In den meisten Fällen ist das Arbeiten mit dem vollständigen Repository der einfachste und verlässlichste Weg, um das Buch zu erkunden. Für einen ersten Einstieg können einzelne Notebooks dennoch hilfreich sein.

````{admonition} Zusätzliche Materialien
:class: seealso
* [Git für Versionsverwaltung verwenden](git)
* [Python](python)  
* [Jupyter Books lokal ausführen](jupyter_book)
* [Editoren für Jupyter Notebooks](editor)
````