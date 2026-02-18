# Publikation auf Zenodo

Zenodo[^url-zenodo] bietet eine Integration mit GitHub an, über die eine Publikation eines bestimmten Zustandes (`commit`) eine GitHub-Repositoriums möglich ist.

```{figure} ../assets/technologie/zenodo_profil_menü.png
---
scale: 35%
align: right
name: fig:zenodo_profil_menü
---

Zugriff auf die GitHub-Integration
ist im Profil-Menü oben rechts hinterlegt.
```

Für die Integration muss eine Person mit genügend Rechten im GitHub-Repositorium eine Verbindung zwischen ihrem Zenodo-Account und ihrem GitHub-Account herstellen. Öffnen Sie dazu das Menü rechts oben über den Pfeil neben Ihrem Account-Namen und wählen Sie dort _GitHub_ aus (siehe {numref}`fig:zenodo_profil_menü`). Folgen Sie den Anweisungen zum Verknüpfen der Accounts.



Sind die Accounts verknüpft, so sehen Sie eine Anleitung, wie ein Repositorium nach Zenodo importiert werden kann. Auf die Schritte wird hier nochmals eingegangen:

1. Vorbereitung des Repositoriums
2. Aktivierung der Integration für ein bestimmtes Repositorium
3. Erstellung eines Releases in GitHub
4. Überprüfung der Metadaten in Zenodo

## Vorbereitung des Repositoriums
Zenodo hat verschiedene Möglichkeiten, Metadaten aus dem Repositorium zu extrahieren und für den Eintrag auf Zenodo zu nutzen. In QUADRIGA nutzen wir die Datei `CITATION.cff`[^url-cff], welche es erlaubt die Metadaten im Repositorium zu definieren. Diese Datei wird auch von GitHub und anderen Werkzeugen genutzt, um Zitationsempfehlungen anzubieten.

````{admonition} CITATION.cff dieses Buches
:class: hinweis, dropdown
```{literalinclude} ../CITATION.cff
:language: yaml
:linenos:
```
````

## Aktivierung der Integration für ein bestimmtes Repositorium

```{figure} ../assets/technologie/zenodo_GitHub_toggle.png
---
scale: 50%
align: right
name: fig:zenodo_GitHub_toggle
---

Deaktiverter und aktivierter Schalter für
den Import neuer Releases in Zenodo.
```

Für jedes Repositorium, für das Sie genügend Rechte haben, können Sie entscheiden, ob Sie neue Releases nach Zenodo importieren wollen (siehe {numref}`fig:zenodo_GitHub_toggle` unten) oder nicht (siehe {numref}`fig:zenodo_GitHub_toggle` oben).

Nutzen Sie diese Funktion, wenn Sie bspw. temporär neue Releases nicht in Zenodo übernehmen wollen.

## Erstellung eines Releases in GitHub

```{figure} ../assets/technologie/GitHub_repo_release.png
---
scale: 50%
align: right
name: fig:GitHub_repo_release
---

Anzeige des aktuellsten Releases
auf der Hauptseite eines
Repositoriums.
```

Releases in GitHub werden über einen `tag` spezifiziert. Diesen Tag können Sie entweder per `git tag`[^url-git-tag] festlegen, oder Sie legen beim Erstellen des Releases einen Tag an.

### Lokale Erstellung eines Tags mit `git tag`

Hinweise zur Erstellung von Tags in der GitHub-Releases-Unterseite finden Sie im nächsten Abschnitt.

Die Option, Tags lokal zu erstellen, wird durch Schritte in der GitHub Action `update-metadata.yml` unterstützt und daher zu bevorzugen. Wenn Sie ein Tag erstellen und pushen, dann wird automatisch die Action ausgelöst. Diese passt, falls nötig die Metadaten-Felder `book-version` und `date-of-last-change` an und erstellt bei Änderung einen neuen Commit. Dann wird der Tag auf den neu-erstellten Commit verschoben.

Schritt für Schritt gehen Sie so vor:
1. Legen Sie das neue Tag an. Im Beispiel nutzen wir die Versionsnummer `0.1.2`.
   ```bash
   $ git tag v0.1.2
   ```
2. "Veröffentlichen" Sie das Tag auf GitHub.
   ```bash
   $ git push origin tag v0.1.2
   ```
3. Die Action `update-metadata.yml` läuft und erstellt ggf. einen neuen Commit. Wird ein Commit erstellt, so wird der Tag auf dem Server "verschoben".

   Warten Sie, bis die Action vollständig ausgeführt wurde.
4. Aktualisieren Sie die Tags in Ihrem lokalen Repositorium.
   ```{admonition} Achtung
   :class: caution
   Achtung, die nachfolgende Operation überschreibt lokale Tags!
   ```
   ```bash
   $ git fetch --tags --all --force
   ```
   Sie können überprüfen, ob Ihre lokalen Tags korrekt sind mit `git log`.

   Wollen Sie nicht alle lokalen Tags überschreiben, so können Sie gezielt Ihre lokale Version löschen und dann nochmals die Tags von GitHub übernehmen.
   ```bash
   $ git tag -d v0.1.2
   $ git fetch --tags --all
   ```
   Damit sollte Ihr Repositorium auf dem gleichen Stand sein wie GitHub.

Tags können auch in GitHub Desktop oder in VS Code erstellt werden. Hierfür gibt es keine gesonderten Anleitungen.


### GitHub-Releases-Unterseite

Klicken Sie entweder auf der Hauptseite des Repositoriums rechts auf _Releases_ (siehe {numref}`fig:GitHub_repo_release`) oder oben neben der Auswahl der _Branches_ auf _Tags_. Stellen Sie auf der nächsten Seite sicher, dass _Releases_ ausgewählt ist.

Auf der _Releases_-Seite werden ggf. existierende Releases angezeigt, welche Sie auch durchsuchen können. Über die Schaltfläche _Draft a new release_ können Sie einen neuen Release erstellen (siehe {numref}`fig:GitHub_releases`).

```{figure} ../assets/technologie/GitHub_releases.png
---
align: center
name: fig:GitHub_releases
---

Menüleiste der _Releases_-Seite mit der Schaltfläche zur Erstellung eines neuen Releases
```

Beachten Sie bei der Erstellung eines neuen Releases die Hinweise in {numref}`fig:GitHub_new_release`. Unter "Choose a tag" kann ein bestehender Tag ausgewählt oder eine neuer erstellt werden (siehe Warnung unten). Tags, die eine Version repräsentieren, sollten einem Standard folgen. Wir empfehlen für QUADRIGA den Standard _Semantic Versioning 2.0.0_[^url-semver].


````{admonition} Wichtig
:class: caution

Bevor Sie diese Option zur Erstellung eines Tags nutzen, stellen Sie bitte sicher, dass in der Metadaten-Datei (`metadata.yml`) die Felder `book-version` und `date-of-last-change` korrekt sind. In `book-version` sollte die Version stehen, welche Sie später im Release angeben (ohne das `v` also `book-version: 0.1.2`, wenn Sie beim Release `v0.1.2` als Tag nutzen). Im `date-of-last-change` sollte das aktuelle Datum stehen.

Erstellen Sie ggf. einen neuen Commit mit diesen Änderungen und beginnen Sie dann den Prozess der Erstellung eines Releases erneut.

Ein Git Tag kann nicht mit einer Zahl beginnen. Typischerweise beginnen Versionstags mit einem `v`. Daher empfehlen wir folgendes Format:
```
v0.1.2
```

````

Dann können Sie Veröffentlichungsinformationen (_release notes_) generieren lassen. Diese müssen ggf. angepasst werden. Der Titel des Releases ist oft eine Wiederholung des Tags, sie können jedoch auch einen _sprechenden Namen_ vergeben. Zu den _release notes_ gehört auch eine Beschreibung der Veränderungen zur letzten veröffentlichten Version.

Ein Release kann als neuester Release markiert werden oder als eine Vorveröffentlichung. Sie können Zwischenstände der Release-Informationen als Entwurf speichern oder den Release veröffentlichen. Veröffentlichen Sie einen Release wird dieser von Zenodo importiert, solange die Importfunktion für das Repositorium aktiviert ist (s.o.). Der Import kann einige Zeit in Anspruch nehmen.

```{figure} ../assets/technologie/GitHub_new_release.png
---
align: center
name: fig:GitHub_new_release
---

Seite zur Erstellung eines neuen Releases.
```

## Überprüfung der Metadaten in Zenodo
Nach einem Release sollten die von Zenodo importierten Informationen überprüft werden. Ggf. müssen Sie in Zenodo und/oder in der Datei `CITATION.cff` angepasst werden. Änderungen in `CITATION.cff` werden mit dem nächsten Release-Import übernommen.

Zenodo stellt auch eine sogenannte Badge zur Verfügung. In den Einstellungen der GitHub-Integration wird diese neben dem Repositorium angezeigt. Klicken Sie auf diese, so öffnet sich eine Ansicht, aus der Sie bspw. Markdown-Code kopieren und Ihre `README.md` einfügen können.

[^url-cff]: <https://citation-file-format.github.io>
[^url-git-tag]: <https://git-scm.com/docs/git-tag>
[^url-semver]: <https://semver.org>
[^url-zenodo]: <https://zenodo.org>
