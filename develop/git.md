---
lang: de-DE
---

# Git – Der De-Facto-Standard der Versionskontrollsoftware

Um die Zusammenarbeit zu unterstützen nutzen wir Git. Git ist eine Versionskontrollsoftware, die es Ihnen erlaubt Snapshots einer Ordner- und Dateistruktur anzulegen, zwischen diesen hin und her zu wechseln und mit parallelen Änderungen an einer Datei umgehen zu können.

Git ist der De-Facto-Standard in der Softwareentwicklung und eignet sich für alle Text-basierten Dateiformate. Mit Binären Dateien wie Audio, Video, PDF, ZIP-Archiven, … kann es auch umgehen, jedoch sind hier einige Funktionalitäten nicht möglich. Große Dateien sollten nicht direkt im Repositorium abgelegt werden.

## Ressourcen
Es gibt viele Ressourcen rund um Git – die meisten sind nur auf Englisch verfügbar. Die nachfolgenden Abschnitte können nur einen kurzen Einblick in die Nutzung von Git bieten. Für alles weitere empfehlen wir Ihnen diese Ressourcen:

- [Julia Evans – Git Cheat-Sheet](https://wizardzines.com/git-cheat-sheet.pdf) (PDF)
- [Scott Chacon & Ben Straub – Pro Git](https://www.git-scm.com/book/en/v2) (Website, PDF, EPUB)
- [Scott Chacon & Ben Straub – Pro Git (deutsche Übersetzung)](https://www.git-scm.com/book/de/v2) (Website, PDF, EPUB)
- [Daniel Shiffman – Git and GitHub for Poets](https://thecodingtrain.com/tracks/git-and-github-for-poets) (Videoreihe)
- [The Turing Way Community – Getting Started With GitHub](https://book.the-turing-way.org/collaboration/github-novice) (Kapitel in einem Jupyter Book)


## Installation
Wenn Sie noch kein Git installiert haben, dann finden Sie die Installationsdateien bspw. auf der [Git Website](https://git-scm.com/downloads). Laden Sie dort die passende Version für Ihr Betriebssystem herunter bzw. folgen Sie den Anleitungen.

Unter Windows wird neben Git selbst noch das Programm *Git Bash* installiert, welches es Ihnen ermöglicht Git über die Kommandozeite zu nutzen, als hätten Sie ein UNIX-artiges Betriebssystem wie Linux oder macOS. Alle unten angegebenen Befehle gehen davon aus, dass Sie diese unter Windows im Programm Git Bash eintippen.

## Github-Account
Um Git für die Erstellung der QUADRIGA-OERs zu nutzen wird ein Github-Account benötigt. Diesen können Sie auf [github.com](https://github.com) anlegen.

Um Änderungen an den QUADRIGA-OERs vornehmen zu können sollte der Account der Organisation [quadriga-dk](https://github.com/quadriga-dk) zugeordnet werden. Die Arbeit über Pull-Requests ist auch möglich und was insbesondere für Externe Mitarbeiter:innen bevorzugt wird.

Nutzen Sie diese Anleitung für die Erstellung von OERs außerhalb des QUADRIGA-Projekts, so benötigen Sie keine zusätzlichen Rechte. Sie können das vorliegende Repositorium als Template für Ihre eigene OER nutzen.

## Die wichtigsten Git Befehle
Git speichert Abbilder/Snapshots einer Ordnerstruktur – eines sogenannten Repositoriums. Ein Snapshot wird in Git als Commit bezeichnet. Ein Commit verweist auf alle Dateien und deren Inhalte zu einem bestimmten (logischen) Zeitpunkt.

Ein Git Repositorium auf einem Server wie Github oder lokal beinhaltet die gleichen Inhalte und Konfigurationsdateien. Jede lokale Kopie des Repositoriums kann genutzt werden um auch einem Server oder anderen Rechner eine Kopie anzulegen. Es können mehrere Server eingerichtet werden – die nachfolgenden Befehle gehen immer davon aus, dass Sie mit einem (GitHub) Server, genannt *origin* arbeiten.

### Clone
Um an einem Repositorium mitzuarbeiten, muss zuerst eine Kopie des Repositoriums lokal abgelegt werden. Das tun Sie mit dem Befehl `git clone`:
```bash
git clone https://github.com/quadriga-dk/Book_Template
```
Das Ergebnis dieses Befehls ist, dass ein Ordner `Book_Template` am aktuellen Ort im Dateisystem angelegt wird und in diesem eine vollständige Kopie des Repositoriums von Github abgelegt wird. Navigieren Sie ggf. vor ausführen des Befehls an eine andere Stelle im Dateisystem. Im Repositorium enthalten ist die gesamte Versionsgeschichte – d.h. alle Commits – sowie alle nötigen Informationen, um das lokale Repositorium nutzen zu können.

Wollen Sie Ihre eigene OER anlegen, dann nutzen Sie bspw. die Template-Funktion auf GitHub. Diese erstellt ein neues Repositorium mit den Inhalten des Templates jedoch ohne die Versionsgeschichte des Template-Repositoriums.

### Fetch
Regelmäßig – insbesondere wenn Sie wissen, dass jemand anderes eine neue Version nach Github hochgeladen hat – sollten Sie `git fetch` nutzen um eine Kopie der Commits auf dem Server herunterzuladen. Ein `git fetch` ändert nichts an dem Commit in dem Sie gerade arbeiten und auch nichts an den Änderungen, die Sie lokal gerade vornehmen. 

Wenn Sie einen anderen Commit auswählen wollen, geht das mit `git checkout`. Das überschreibt ggf. aktive Änderungen, die Sie noch nicht gespeichert – commit-tet – haben (s.u.).

### Pull
Wenn Sie auf den gleichen Stand wechseln wollen wie der Server, dann können Sie `git pull` nutzen. Dies geht nur reibungslos, wenn Sie lokal keine Änderungen gemacht haben, die in Konflikt stehen mit Änderungen, die auf dem Server abgelegt waren. Um mit Konflikten umzugehen gibt es den sogenannten Stash, auf welchen hier vorerst nicht eingegangen wird. Sie kannst Konflikte zwischen Commits mit Merge beheben (s.u.) oder über ein sogenannten Rebase.

### Add
Während Sie lokal arbeiten ändert sich nicht automatisch der aktuelle Snapshot. Stattdessen merkt sich Git Ihre Änderungen separat – man sagt, die Änderungen sind *unstaged*. Sie können sich über `git status` anzeigen lassen, welche Dateien Sie lokal geändert haben. Mit `git diff` können Sie sich im Detail Ihre inhaltlichen Änderungen anzeigen lassen. Wenn Sie eine der Änderungen für einen Commit vormerken wollen, dann geht das mit `git add` – die Änderungen sind dann *staged*.

Um bspw. eine Änderung in dieser Datei für einen Commit vorzumerken würden Sie diesen Befehl nutzen:
```bash
git add develop/git.md
```

Über `git status` sehen Sie dann, dass die Inhalte vorgemerkt sind. Sie können vorgemerkte Änderungen auch wieder entfernen – die Änderung bleibt lokal vorhanden – oder Änderungen ganz verwerfen und eine Datei auf den Zustand aus dem aktiven Commit zurücksetzen – hier droht Datenverlust!

### Commit
Wenn Sie vorgemerkte Änderungen als Snapshot speichern wollen um diese bspw. auf Github hochzuladen, dann müssen Sie einen Commit erstellen. Dies geht mit `git commit`. Ein Commit beinhaltet alle Ordner und Dateien in einem bestimmten Zustand. Dieser Zustand ist zusammengesetzt aus dem/ vorherigen Commit(s) sowie allen für den Commit vorgemerkten Änderungen. Ein Commit hat dabei einen oder mehrere Vorgänger, wodurch eine Baumstruktur aus Commits entsteht.

Wichtig für die Zusammenarbeit ist auch, dass ein Commit eine *Commit Message* hat, in der Sie kurz festhalten, welche Änderungen im Commit vorgenommen wurden und warum. Hier können Entscheidungsprozesse und Diskussionen dokumentiert werden. Oft werden in Commit Messages auch IDs von Issues vermerkt, in denen bspw. ein Fehler dokumentiert oder ein Feature diskutiert wurde.

Sie können eine Commit Message gleich in den Befehl einfügen, wenn Sie die Option `-m` nutzen. Ansonsten wird ein Editor (normalerweise vim – das sollten Sie ggf. anpassen) geöffnet, in dem Sie die Message verfassen können.
```bash
git commit -m "Add introduction to git"
```

### Push
```{margin}
Statt eines `git merge` besteht hier auch die Möglichkeit ein Rebase zu nutzen. Hier gibt es verschiedene Möglichkeiten auf die in dieser Anleitung nicht weiter eingegangen wird.
```
Wenn Sie einen Commit erstellt haben, ist er vorerst nur lokal vorhanden. Um ihn auf den Server hochzuladen müssen Sie `git push` nutzen – dies lädt den Commit standardmäßig auf den Server mit dem internen Namen *origin* hoch, also auf den Server, von dem Sie geklont haben. Vor diesem Schritt empfiehlt es sich fast immer zuerst ein `git pull` durchzuführen und dann ggf. existierende Konflikte bspw. mit `git merge` zu beheben, bevor Sie mit `git push` Ihre Änderungen tatsächlich auf den Server hochladen.

Ein anderer Weg ist es, Commits in einem Branch zu pushen und dann bspw. über die Github Oberfläche diese Änderungen wieder in den *main*-Branch zu "ziehen". Das ist zu empfehlen, wenn Sie lange und über mehrere Commits an einer Änderung arbeiten, die dann als ganzes in die OER integriert werden soll (s.u.).

### Merge
`git merge` pflegt Änderungen eines Commits bzw. eines Branches in einen anderen Commit/Branch ein und erzeugt dazu einen sogenannten Merge Commit. Funktioniert das nicht automatisch, so müssen Sie alle Konflikte von Hand beheben. (Eine andere Option des Zusammenführens ist hier wieder `git rebase`.)

## Branch und switch
Mit einem Branch können Sie einen Commit (bzw. eine Reihe von Commits) benennen, sodass Sie ihn wieder leicht finden können. Mit `git branch -c tutorial` erzeugen Sie einen Branch. Mit `git switch tutorial` wechseln Sie zu dem Branch. Commits, die Sie erstellen, während Sie im Branch sind, werden automatisch zum Branch hinzugefügt. Dies ermöglicht es, getrennt von Änderungen anderer Personen zu arbeiten oder verschiedene Optionen parallel auszuprobieren. Wenn Sie mit dem Zustand des Branches zufrieden sind, können Sie ihn wieder mit dem normalen Entwicklungsbranch (meistens entweder *main* oder *master* genannt) zusammenführen. Ein Branch kann lokal bleiben oder auf den Server synchronisiert werden, sodass andere auch an dem Feature arbeiten können oder Ihren Arbeitsstand sehen können.

```{admonition} Übung
:class: tip
1. Gehen Sie auf die [Github-Seite des OER-Templates](https://github.com/quadriga-dk/Book_Template).
2. Stellen Sie sicher, dass Sie eingeloggt sind und wählen Sie dann *Fork > Create a new Fork*.
3. Folgen Sie den Anweisungen um eine spezielle Kopie des Templates in Deinem Github-Account zu erstellen, die Fork genannt wird. Ein Fork ist verbunden mit dem sogenannten *Upstream* Repositorium und kann Änderungen aus diesem bei sich wieder Einpflegen und Vorschläge für Änderungen (sog. Pull Requests) anbieten.
4. Nutzen Sie nun `git clone` um eine Kopie Ihres Forks auf Ihrer lokalen Festplatte zu erstellen.
5. Erzeugen Sie einen Branch mit dem Namen `tutorial` und wechseln Sie in diesen.
6. Erstellen Sie eine Markdown-Datei und schreiben Sie in diese etwas Text.
7. Fügen die Markdown-Datei dem Inhaltsverzeichnis `_toc.yml` hinzu.
8. Merken die Änderungen für einen Commit vor und erstellen dann den Commit. Denken Sie an eine passende Commit Message.
9. Was passiert, wenn Sie `git push` ausführen?
10. Wechseln Sie in den Branch `main`.
11. Mergen Sie die Änderungen aus dem Branch `tutorial` nach `main`.
12. Führen Sie noch einmal `git push` durch. Was passiert dieses Mal?
13. Sehen Sie sich die 5 neuesten Commits in der Versionsgeschichte an mit `git log -5`.

### Bonus
14. Aktivieren Sie Github Pages und Github Actions in Ihrem Fork um automatisch das Jupyter Book bauen zu lassen. Dazu muss Ihr Fork öffentlich normalerweise sichtbar sein.

```

## Branches und Commits
```{figure} ../assets/develop/git/Git_branches_ueber_die_Zeit.svg
---
align: left
width: 100%
---
Darstellung einer zeitlichen Entwicklung mehrerer Commits und Branches. Ausgehend vom Branch *main* wird ein Branch *tutorial* angelegt. In diesem wird ein Commit gespeichert. Dann wird in *main* ein anderer Commit gespeichert. Im nächsten Schritt wird noch ein Commit im Branch *tutorial* erzeugt. Am Ende wird der Branch *tutorial* in den Branch *main* gemerget.
```

