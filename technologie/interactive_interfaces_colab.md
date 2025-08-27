# Interaktive Rechenumgebungen mit Google Colab

Da Jupyter Books auf Jupyter-Notebooks oder ausführbaren Markdown-Dateien basieren, ist es möglich, über einen Launch-Button direkt in der Cloud interaktive Jupyter-Sessions zu starten. So können Inhalte in einer vertrauten Coding-Umgebung live ausprobiert werden. Wir verwenden in dieser Vorlage Google Colab, eine kostenlose Cloud-Lösung für Jupyter Notebooks. Im Folgenden erläutern wir die wichtigsten Aspekte der Nutzung dieser interaktiven Funktionen.


## Technische Konfiguration
Damit die Launch-Buttons in Ihrem Jupyter Book erscheinen, muss die Datei `_config.yml` entsprechend konfiguriert werden. Fügen Sie folgende Zeilen in Ihre `_config.yml` ein:

```yaml
launch_buttons:
    # Konfiguration für Google Colab
    colab_url: https://colab.research.google.com
```

Diese Konfiguration aktiviert die Google Colab Launch-Buttons für alle kompatiblen Notebooks in Ihrem Buch.


## Google Colab: Grundlegende Konzepte und Herausforderungen

### 🚀 Launch Button
Wenn Sie den "Launch > Colab" button betätigen, wird ausschließlich das entsprechende Notebook in Google Colab geöffnet - nicht der gesamte Projektordner. Dies ist ein wichtiger Aspekt, der bestimmte manuelle Anpassungen erforderlich macht.

### Häufige Herausforderungen und Lösungsansätze

#### Fehlende Python-Pakete
Wenn Sie eine Fehlermeldung über ein fehlendes Paket erhalten (beispielsweise `ModuleNotFoundError: No module named 'jupyterquiz'`), müssen Sie dieses nachinstallieren. Der Prozess ist wie folgt:

- Fügen Sie folgenden Befehl am Anfang Ihres Notebooks ein:
  ```python
  !pip install package_name
  ```
  
#### Zugriff auf Projektdateien
Da Colab nur die einzelne Notebook-Datei öffnet, hat es keinen direkten Zugriff auf andere Dateien aus dem Projektordner. Hier bieten sich zwei einfache Lösungswege an:

1. Für Dateien in einem öffentlichen GitHub-Repository:
   ```python
   !wget https://raw.githubusercontent.com/username/repository/main/ordner/dateiname
   ```

2. Direktes Hochladen von Dateien:
   - Klicken Sie auf das Ordner-Symbol in der linken Seitenleiste
   - Laden Sie Ihre Datei per Drag & Drop oder über den Upload-Button hoch


```{admonition} Tipps
:class: keypoint
1. Führen Sie stets alle Setup-Zellen am Anfang des Notebooks aus
2. Installieren Sie fehlende Pakete mit `!pip install`
3. Laden Sie benötigte Dateien hoch, bevor Sie Zellen ausführen, die diese verwenden
4. Sichern Sie wichtige Arbeitsergebnisse in Google Drive oder auf Ihrem lokalen Rechner
```



## Alternative Plattformen

Neben Google Colab existieren weitere Plattformen für interaktive Notebooks:

- **Binder**: Ermöglicht die Ausführung von Notebooks ohne Installation und kann ganze Projektordner öffnen

- **JupyterHub**: Wird häufig von Universitäten und Organisationen für gehostete Notebooks eingesetzt

Google Colab bietet für die meisten Lernenden den einfachsten Einstieg und wird daher in diesem Lehrbuch als primäre Plattform verwendet.


```{admonition} Zusätzliche Materialien
:class: seealso
Für detaillierte Informationen zur Konfiguration von Launch-Buttons in Jupyter Book empfehlen wir die offizielle <a href="https://jupyterbook.org/en/stable/interactive/launchbuttons.html" class="external-link" target="_blank">Jupyter Book Dokumentation zu Launch Buttons</a>. Diese enthält wichtige technische Details zur Integration verschiedener interaktiver Plattformen in Ihr eigenes Jupyter Book.

Für die praktische Arbeit mit Google Colab empfehlen wir zusätzlich die  <a href="https://colab.research.google.com/notebooks/basic_features_overview.ipynb" class="external-link" target="_blank">Colab Dokumentation</a>.
```