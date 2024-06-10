# Git – Der De-Facto-Standard der Versionskontrollsoftware

Um die Zusammenarbeit zu unterstützen nutzen wir Git. Git ist eine Versionskontrollsoftware, die es erlaubt Snapshots einer Ordner- und Dateistruktur anzulegen, zwischen diesen hin und her zu wechseln und mit parallelen Änderungen an einer Datei umgehen zu können.

Git ist der De-Facto-Standard in der Softwareentwicklung und eignet sich für alle Text-basierten Dateiformate. Mit Binären Dateien wie Audio, Video, PDF, ZIP-Archiven, … kann es auch umgehen, jedoch sind hier einige Funktionalitäten nicht möglich. Große Dateien sollten nicht direkt im Repositorium abgelegt werden.

## Installation
Wenn Du noch kein Git installiert hat, dann findest Du die Installationsdateien bspw. auf der [Git Website](https://git-scm.com/downloads). Lade dort die passende Version für Dein Betriebssystem herunter bzw. folge den Anleitungen.

Unter Windows wird neben Git selbst noch das Programm *Git Bash* installiert, welches Dir ermöglicht Git über die Kommandozeite zu nutzen als hättest Du ein UNIX-artiges Betriebssystem wie Linux oder macOS. Alle unten angegebenen Befehle gehen davon aus, dass Du sie unter Windows im Programm Git Bash eintippst.

## Github-Account
Um Git für die Erstellung der QUADRIGA-OERs zu nutzen wird ein Github-Account benötigt. Dieser kann auf [github.com](https://github.com) erstellt werden.

Um Änderungen an den QUADRIGA-OERs vornehmen zu können sollte der Account der Organisation [quadriga-dk](https://github.com/quadriga-dk) zugeordnet werden. Die Arbeit über Pull-Requests ist auch möglich und was insbesondere für Externe Mitarbeiter\*innen bevorzugt wird.

## Die wichtigsten Git Befehle
Git speichert Abbilder/Snapshots einer Ordnerstruktur – eines sogenannten Repositoriums. Ein Snapshot wird in Git als Commit bezeichnet. Ein Commit verweist auf alle Dateien und deren Inhalte zu einem bestimmten (logischen) Zeitpunkt.

Ein Git Repositorium auf einem Server wie Github oder lokal beinhaltet die gleichen Inhalte und Konfigurationsdateien. Jede lokale Kopie des Repositoriums kann genutzt werden um auch einem Server oder anderen Rechner eine Kopie anzulegen. Es können mehrere Server eingerichtet werden – die nachfolgenden Befehle gehen immer davon aus, dass mit einem (Github) Server, genannt *origin* gearbeitet wird.

### Clone
Um an einem Repositorium mitzuarbeiten muss zuerst eine Kopie des Repositoriums lokal abgelegt werden. Das geschieht mit dem Befehl `git clone`:
```bash
git clone https://github.com/quadriga-dk/Book_Template
```
Das Ergebnis dieses Befehls ist, dass ein Ordner `Book_Template` am aktuellen Ort im Dateisystem angelegt wird und in diesem eine vollständige Kopie des Repositoriums von Github abgelegt wird. Navigiere ggf. vor ausführen des Befehls an eine andere Stelle im Dateisystem. Im Repositorium enthalten ist die gesamte Versionsgeschichte – d.h. alle Commits – sowie alle nötigen Informationen, um das lokale Repositorium nutzen zu können.

### Fetch
Regelmäßig – insbesondere wenn Du weißt, dass jemand anderes eine neue Version nach Github hochgeladen hat – solltest Du `git fetch` nutzen um eine Kopie der Commits auf dem Server herunterzuladen. Ein `git fetch` ändert nichts an dem Commit in dem Du gerade arbeitest und auch nichts an den Änderungen, die du lokal gerade machst. 

Wenn Du einen anderen Commit auswählen willst geht das mit `git checkout`. Das überschreibt ggf. aktive Änderungen, die du noch nicht gespeichert hast (s.u.).

### Pull
Wenn Du auf den gleichen Stand wechseln willst wie der Server, dann kannst Du `git pull` nutzen. Dies geht nur reibungslos, wenn Du lokal keine Änderungen gemacht hast, die in Konflikt stehen mit Änderungen, die auf dem Server abgelegt waren. Um mit Konflikten umzugehen gibt es den sogenannten Stash, auf welchen hier vorerst nicht eingegangen wird. Du kannst Konflikte zwischen Commits mit Merge beheben (s.u.).

### Add
Während Du lokal arbeitest ändert sich nicht automatisch der aktuelle Snapshot. Stattdessen merkt sich Git diese Änderungen separat – man sagt, die Änderungen sind *unstaged*. Du kannst Dir über `git status` anzeigen lassen, welche Dateien Du lokal geändert hast. Mit `git diff` kannst du dir inhaltliche Änderungen anzeigen lassen. Wenn Du eine der Änderungen für einen Commit vormerken willst, dann geht das mit `git add` – die Änderungen sind dann *staged*.

Um bspw. eine Änderung in dieser Datei für einen Commit vorzumerken nutze diesen Befehl:
```bash
git add develop/git.md
```

Über `git status` siehtst Du dann, dass Inhalte vorgemerkt sind. Du kannst vorgemerkte Änderungen auch wieder entfernen – die Änderung bleibt lokal vorhanden – oder Änderungen ganz verwerfen und eine Datei auf den Zustand aus dem aktiven Commit zurücksetzen – hier droht Datenverlust!

### Commit
Wenn Du vorgemerkte Änderungen als Snapshot speichern willst um sie bspw. auf Github hochzuladen, dann musst Du einen Commit erstellen. Dies geht mit `git commit`. Ein Commit beinhaltet alle Ordner und Dateien in einem bestimmten Zustand. Ein Commit hat zudem einen oder mehrere Vorgänger, wodurch eine Baumstruktur aus Commits entsteht.

Wichtig für die Zusammenarbeit ist auch, dass ein Commit eine *Commit Message* hat, in der Du kurz festhältst, welche Änderungen im Commit vorgenommen wurden und warum. Hier können Entscheidungsprozesse und Diskussionen dokumentiert werden. Oft werden in Commit Messages auch IDs von Issues vermerkt, in denen bspw. ein Fehler dokumentiert oder ein Feature diskutiert wurde.

Du kannst eine Commit Message gleich in deinen Befehl einfügen, wenn Du `-m` nutzt. Ansonsten wird ein Editor (normalerweise vim – das solltest Du ggf. anpassen) geöffnet, in dem die Message verfassen kannst.
```bash
git commit -m "Add introduction to git"
```

### Push
Wenn Du einen Commit erstellt hast ist er vorerst nur lokal vorhanden. Um ihn auf den Server hochzuladen musst Du `git push` nutzen – dies lädt den Commit standardmäßig auf den Server mit dem internen Namen *origin* hoch, also dem Server, von dem Du geklont hast. Vor diesem Schritt empfiehlt es sich fast immer zuerst ein `git pull` durchzuführen und dann ggf. existierende Konflikte bspw. mit `git merge` zu beheben, bevor Du mit `git push` Deine Änderungen tatsächlich auf den Server hochlädst.

Ein anderer Weg ist es, Commits in einem Branch zu pushen und dann bspw. über die Github Oberfläche diese Änderungen wieder in den *main*-Branch zu "ziehen". Das ist zu empfehlen, wenn lange und über mehrere Commits an einer Änderung gearbeitet wird, die dann als ganzes in die OER integriert werden soll (s.u.).

### Merge
`git merge` pflegt Änderungen eines Commits bzw. eines Branches in einen anderen Commit/Branch ein und erzeugt dazu einen sogenannten Merge Commit. Funktioniert das nicht automatisch, so musst Du alle Konflikte von Hand beheben. (Eine andere Option des Zusammenführens nennt sich `git rebase`.)

## Branch und switch
Mit einem Branch kannst Du einen Commit (bzw. eine Reihe von Commits) benennen, sodass Du ihn wieder leicht finden kannst. Mit `git branch -c tutorial` erzeugst Du einen Branch. Mit `git switch tutorial` wechselst Du zu dem Branch. Commits, die du erstellts während du im Branch bist, werden automatisch zum Branch hinzugefügt. Dies ermöglicht es, getrennt von Änderungen anderer zu arbeiten. Wenn Du mit dem Zustand des Branches zufrieden bist, kannst Du ihn dann wieder mit dem normalen Entwicklungsbranch (meistens entweder *main* oder *master* genannt) zusammenführen. Ein Branch kann lokal bleiben oder auf den Server synchronisiert werden, sodass andere auch an dem Feature arbeiten können.


## Ressourcen
Es gibt viele Ressourcen rund um Git – die meisten sind nur auf Englisch verfügbar.
- [Julia Evans – Git Cheat-Sheet](https://wizardzines.com/git-cheat-sheet.pdf) (PDF)
- [Scott Chacon & Ben Straub – Pro Git](https://www.git-scm.com/book/en/v2) (Website, PDF, EPUB)
- [Scott Chacon & Ben Straub – Pro Git (deutsche Übersetzung)](https://www.git-scm.com/book/de/v2) (Website, PDF, EPUB)
- [Daniel Shiffman – Git and GitHub for Poets](https://thecodingtrain.com/tracks/git-and-github-for-poets) (Videoreihe)


## Übung:
1. Gehe auf die [Github-Seite des OER-Templates](https://github.com/quadriga-dk/Book_Template).
2. Stelle sicher, dass du eingeloggt bist und wähle dann *Fork > Create a new Fork*.
3. Folge den Anweisungen um eine Kopie spezielle des Templates in Deinem Github-Account zu erstellen, die Fork genannt wird. Ein Fork ist verbunden zum sogenannten *Upstream* Repositorium und kann Änderungen aus diesem bei sich wieder Einpflegen und Vorschläge für Änderungen (sog. Pull Requests) anbieten.
4. Nutze nun `git clone` um eine Kopie deines Forks auf deiner lokalen Festplatte zu erstellen.
5. Erzeuge einen Branch mit dem Namen `tutorial` und wechsle in diesen.
6. Erstelle eine Markdown-Datei schreibe etwas Text in diese.
7. Füge die Markdown-Datei dem Inhaltsverzeichnis `_toc.yml` hinzu.
8. Merke die Änderungen für einen Commit vor und erstelle dann den Commit.
9. Was passiert, wenn du `git push` ausführst?
10. Wechsle in den Branch `main`.
11. Merge die Änderungen aus dem Branch `tutorial` nach `main`.
12. Führe noch einmal `git push` durch. Was passiert dieses mal?
13. Sie dir die 5 neuesten Commits in der Geschichte an mit `git log -5`.

### Bonus
14. Aktiviere Github Pages und Github Actions in deinem Fork um automatisch das Jupyter Book bauen zu lassen.


