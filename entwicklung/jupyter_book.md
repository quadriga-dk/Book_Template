---
lang: de-DE
---
# Jupyter Book

## Einrichtung der lokalen Entwicklungsumgebung


### Environments
Es gibt verschiedene Möglichkeiten sogenannte *virtual environments* zu erstellen. Wir erläutern hier zwei Optionen.

#### `python3 -m venv`
Mit dem Befehl `python3 -m venv` können Sie ein virtuelles Environment erstellen, das speziell für Ihr Projekt geeignet ist. Dieses Environment ermöglicht es Ihnen, Python-Pakete und -Bibliotheken isoliert vom globalen Python-System zu installieren und zu verwalten. Dies ist besonders nützlich, um Konflikte zwischen verschiedenen Projekten zu vermeiden und die Reproduzierbarkeit Ihrer Arbeit zu gewährleisten.

Um ein neues virtuelles Environment zu erstellen, navigieren Sie in das Verzeichnis Ihres Projekts und führen Sie den folgenden Befehl aus:

```bash
python3 -m venv venv
```

Dies erzeugt einen Ordner venv im aktuellen Verzeichnis, in dem alle notwendigen Dateien für das virtuelle Environment gespeichert werden.

Um das Environment zu aktivieren, verwenden Sie den folgenden Befehl:

- **Unter Unix oder MacOS**: Führen Sie im Terminal aus:

  ```bash
  source venv/bin/activate
  ```

- **Unter Windows**: Führen Sie in der Eingabeaufforderung aus:

  ```
  venv\Scripts\activate
  ```

Nach der Aktivierung sehen Sie in der Kommandozeile eine Markierung wie `(venv)`, die anzeigt, dass die virtuelle Umgebung aktiv ist.


Stellen Sie sicher, dass die virtuelle Umgebung aktiviert ist, und installieren Sie dann die für Ihr Projekt erforderlichen Pakete:

```bash
pip install -r requirements.txt
```
Damit sollte der Befehl `jb` für Jupyter Book zur Verfügung stehen. Klappt das nicht, dann deaktivieren Sie das Environment einmal mit `deactivate` und aktivieren Sie es dann wieder.


#### Anaconda
Wenn Sie Anaconda installieren, wird automatisch ein virtual environment mit dem Namen `base` eingerichtet. Dieses ist bspw. im Anaconda Command Prompt automatisch aktiviert. In einem virtual environment (oft auch virtual env oder nur venv genannt) kann genau festgelegt werden, welche Programme und Programmbibliotheken in welchen Versionen verwendet werden sollen. Das ist besonders wichtig für aufwendige Konfigurationen oder für die Reproduzierbarkeit.

Wir nutzen das Programm `conda`, um Environments anzulegen, wobei wir Ihnen empfehlen, ein Environment für genau ein Projekt – in diesem Fall eine OER – zu nutzen.

Sind Sie in einem Environment, so können Sie dieses mit `conda deactivate` deaktivieren.

Sie können "globale" Environments anlegen, jedoch empfehlen wir projekt-spezifische Environments, die im Ordner der OER abgelegt werden. Git ist im Template so konfiguriert, dass der Ordner `conda` ignoriert wird.

Legen Sie ein lokales Environment an, in welchem Python3 installiert ist, mit dem nachfolgenden Befehl. Wählen Sie dabei die Standardinstallation.
```bash
conda create -p ./conda python=3
```
In der Windows Eingabeaufforderung wäre das:
```
conda create -p .\conda python=3
```
Dies erzeugt einen Ordner `conda` im aktuellen Verzeichnis, in dem alle nötigen Programme wie Python installiert werden.

Mit `conda activate ./conda` können Sie das Environment aktivieren. Dadurch werden die im Environment installierten Programme und Programmbibliotheken innerhalb des Terminals korrekt zur Verfügung gestellt. Nutzen Sie einen Editor, so müssen Sie dort ggf. auch das Environment aktivieren. Wenn Sie jetzt bspw. `python3` ausführen, dann wird der Python-Interpreter aus dem Environment genutzt.

Installieren Sie nun alle für das Projekt/die OER benötigten Programme und Programmbibliotheken mit `pip install -r requirements.txt`. Damit sollte der Befehl `jb` für Jupyter Book zur Verfügung stehen. Klappt das nicht, dann deaktivieren Sie das Environment einmal und aktivieren Sie es dann wieder.

## Lokale Entwicklung

Wenn Sie im lokalen Ordner Ihres Git Repositoriums sind, können Sie die Webansicht der OER mit `jb build .` neu bauen lassen. Am Ende des Befehls finden Sie einen `file://`-Link zur Startseite, den Sie in einem Browser öffnen können. Wenn das nicht klappt, oder Sie besondere Anforderungen haben, dann nutzen Sie am besten einen lokalen HTTP-Server, um die Dateien zu hosten (bspw. `python3 -m http.server -d _build/html`) und gehen Sie im Browser zur angezeigten URL.

Wenn Sie lokale Dateien anpassen – bspw. wenn Sie an Ihrem Buch weiterschreiben – müssen Sie immer zuerst `jb build .` ausführen, bevor die Änderungen im Browser sichtbar werden. Gibt es hierbei Probleme, so kann es helfen zuerst "aufzuräumen" mit `jb clean .`. Ist Cacheing aktiviert (`execute.execute_notebooks: cache` in `_config.yml`), so kann der Cache für ausgeführte Jupyter Notebooks mit `jb clean --all .` geleert werden. Wenn Sie danach wieder `jb build .` ausführen, so werden alle Seiten, auch die, die Sie nicht geändert haben, neu gebaut. Dieser Schritt des Aufräumens und Bauens mittels `jb clean . && jb build .` ist insbesondere dann nötig, wenn Sie etwas am Inhaltsverzeichnis (`_toc.yml`) geändert haben.

## Updates der verwendeten Programmbibliotheken
In der Datei `requirements.txt` werden die jeweils verwendeten Versionen der Programmbibliotheken hinterlegt. Ändert sich die Datei, so sollten Sie Ihre lokale Entwicklungsumgebung aktualisieren.

Stellen Sie dazu zuerst sicher, dass Sie im Virtuellen Environment der OER sind (bspw. mit `conda activate ./conda` im Wurzelverzeichnis der OER). Führen Sie dann den folgenden Befehl aus:
```sh
$ pip install -r requirements.txt --upgrade
```
Dieser Befehl installiert ggf. neu benötigte Programmbibliotheken und aktualisiert bereits installierte entsprechend der Versions-Vorgaben in der Datei `requirements.txt`.

## Änderung der OER auf Github

Kleine Änderungen können auch direkt auf Github durchgeführt werden. Jede Datei hat rechts oben ein Stift-Symbol, wodurch Sie in einen Bearbeitungsmodus gelangen. Ein Speichern ist hier automatisch ein Commit – denken Sie an eine gute Commit Message.


## Ressourcen
