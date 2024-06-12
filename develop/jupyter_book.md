# Jupyter Book

## Einrichtung der lokalen Entwicklungsumgebung


### Environments 
Wenn Du Anaconda installierst, wird automatisch ein sogenanntes *virtual environment* mit dem Namen `base` eingerichtet. Dieses ist bspw. im Anaconda Command Prompt automatisch aktiviert. In einem virtual environment (oft auch virtual env oder nur venv genannt) kann genau festgelegt werden, welche Programme und Programmbibliotheken in welchen Versionen verwendet werden sollen. Das ist besonders wichtig für aufwendige Konfigurationen oder für die Reproduzierbarkeit.

Wir nutzen das Programm `conda` um Environments anzulegen, wobei es sich empfielt ein Environment nur für genau ein Projekt – in diesem Fall eine OER – zu nutzen.

Bist Du in einem Environment kannst Du dieses mit `conda deactivate` deaktivieren.

Du kannst "globale" Environments anlegen, jedoch empfehlen wir hier projekt-spezifische Environments, die im Ordner der OER abgelegt werden. Git ist im Template so konfiguriert, dass der Ordner `conda` ignoriert wird.

Lege ein lokales Environment an in dem Python3 installiert ist mit diesem Befehl. Installiere die Standardeinstellungen.
```bash
conda create -p ./conda
```
Unter Windows wäre das:
```cmd
conda create -p .\conda
```
Dies erzeugt einen Ordner `conda` im aktuellen Verzeichnis, in dem alle nötigen Programme wie Python installiert werden.

Mit `conda activate ./conda` kannst Du das Environment aktivieren. Dadurch werden die im Environment installierten Programme und Programmbibliotheken innerhalb des Terminals korrekt zur Verfügung gestellt. Wenn Du jetzt bspw. `python3` ausführst, dann wird das Python aus dem Environment genutzt.

Installiere nun alle für das Projekt/die OER benötigten Programme und Programmbibliotheken mit `pip install -r requirements.txt`. Damit sollte der Befehl `jb` für Jupyter Book zur Verfügung stehen. Klappt das nicht, dann deaktiviere das Environment einmal und aktiviere es dann wieder.

## Lokale Entwicklung
Wenn Du im lokalen Ordner deines Git Repositoriums bist kannst Du die OER mit `jb build .` neu bauen lassen. Am Ende des Befehls findest Du einen `file://`-Link zur Startseite, den Du in einem Browser öffnen kannst. Wenn das nicht klappt, dann nutze einen lokalen HTTP-Server um die Dateien zu hosten (bspw. `python3 -m http.server -d _build/html`) und gehe im Browser zur angezeigten URL.

Wenn Du lokale Dateien anpasst musst Du immer zuerst `jb build .` ausführen, bevor die Änderungen im Browser sichtbar werden. Gibt es hierbei einmal Probleme kann es helfen zuerst "aufzuräumen" mit `jb clean .`. Wenn Du danach wieder `jb build .` ausführst, so werden alle Seiten, auch die, die Du nicht geändert hattest, neu gebaut.

## Änderung der OER auf Github
Kleine Änderungen können auch direkt auf Github durchgeführt werden. Jede Datei hat rechts oben ein Stift-Symbol, wodurch Du in einen Bearbeitungsmodus gelangst. Ein speichern ist hier automatisch ein Commit – denke an eine gute Commit Message.


## Ressourcen
