# QUADRIGA OER Template

[Markdown-Cheatsheet für Jupyter Book](https://jupyterbook.org/en/stable/reference/cheatsheet.html)

Dieses Repositorium dient als Vorlage für [QUADRIGA](https://quadriga-dk.github.io) OERs, die mit [Jupyter Book](https://jupyterbook.org) geschrieben werden.

## Nutzung der Vorlage

Erstellen Sie ein neues Repositorium mit dem Namen des neuen Buchs in der GitHub-Organisation quadriga-dk. Nutzen Sie dazu entweder die GitHub-Funktion "Use this template" oder erstellen Sie ein leeres und kopieren Sie die Inhalte des Templates (bspw. Download als `.zip`-Datei) in das neue Repositorium. Passen Sie dann die Dateien `_config.yml` und `_toc.yml` sowie ggf. die Datei `.github/workflows/deploy-book.yml` auf Ihr neues Buch an. Achten Sie darauf, dass Ihr neues Buch keine direkte Verbindung zum Template mehr hat und Änderungen im Template ggf. "von Hand" in Ihre OER überführt werden müssen.

Übernehmen Sie Änderungen im Styling/Layout in der Vorlage auch in Ihrem Buch. Bei wichtigen Änderungen wird ggf. auch ein Pull-Request an Ihre Bücher durch die Template-Autor:innen gestellt werden.

### Erstellung der Inhalte

Jupyter Book kann standardmäßig Inhalte verarbeiten, die in Markdown, MyST und Jupyter Notebook geschrieben wurden. Dabei werden diese Inhalte nur in der Website angezeigt, wenn Sie diese in der Datei `_toc.yml` explizit in die Struktur aufgenommen haben.

## Lokale Entwicklung

Ist die Github Action für Github Pages korrekt konfiguriert, so ist die Arbeit in der GitHub-Oberfläche möglich – wenn sie auch mit großen Wartezeiten verbunden ist. Allerdings empfehlen wir Ihnen immer eine lokale "Entwicklungsumgebung".

Wir empfehlen Ihnen dabei dieses Vorgehen:
- Installieren Sie [Anaconda](https://www.anaconda.com/download) um eine Python-Umgebung auf Ihrem Rechner zu installieren. Falls Sie schon eine Python-Umgebung haben, können Sie diesen Schritt ggf. überspringen.
- Klonen Sie das Repositorium, an dem Sie arbeiten wollen. Bspw.: `git clone https://github.com/quadriga-dk/Book_Template`
- In einem Terminal, wechseln Sie in den Order des Repositoriums und erstellen Sie ein lokales *virtual environment*. (Wir nutzen `conda`, aber andere Tools sind möglich, falls Sie schon mit diesen vertraut sind.) Führen Sie dazu diesen Befehl aus: `conda create -p conda python=3`. Dies erstellt eine neue Virtuelle Umgebung im Ordner `./conda/` in welchem alle für Ihr Buch notwendigen Bibliotheken installiert werden können. (Der Ordner `conda` wird durch die Konfiguration in der Datei `.gitignore` nicht mit Git versioniert, sodass die jeweils korrekte Version aller Software für Ihr Betriebssystem installiert werden kann.)
- Aktivieren Sie nun die Virtuelle Umgebung mit `conda activate ./conda` (und überprüfen Sie, ob alles funktioniert hat mit `which pip`.)
- Installieren Sie dann die für Ihr Buch benötigte Software mit `pip install -r requirements.txt`.
  - Es kann nötig sein, dass Sie nach der Installation einmal die Umgebung deaktivieren und wieder aktivieren müssen, damit Du auf alle Software zugreifen können. Das geht mit `conda deactivate` gefolgt von `conda activate ./conda`.
- Nun haben Sie alle Anforderungen installiert und Sie können das Jupyter Book lokal generieren mit `jb build .`.
  - Machmal kann es nötig sein "aufzuräumen", bevor Sie eine neue Version generieren. Das geht mit `jb clean .`. Sie können auch beide Befehle nacheinander ausführen mit `jb clean . && jb build .`.
- Die generierte HTML-Version des Buchs können Sie nun im Unterordner `_build/html/` finden. Um die Entwicklung zu beschleunigen, kann es hilfreich sein, wenn Sie das Buch über einen lokalen HTTP-Server in Ihrem Browser verfügbar machen. Öffnen Sie dazu ein neues Terminal(-Fenster) und führen Sie diesen Befehl aus: `python3 -m http.server -d _build/html/`. Dies startet einen HTTP-Server, der die Inhalte des HTML-Ordners (standardmäßig) unter `http://localhost:8000/` anbietet.
