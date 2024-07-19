---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
lang: de-DE
---
```{code-cell} ipython3
:tags: [remove_cell]
from jupyterquiz import display_quiz

import sys
sys.path.append("..")
from quadriga_config import colors
```
# Unix

Viele der Kommandozeilenbefehle, die in dieser Anleitung genutzt werden, gehen von einer Unix-Umgebung aus. In einer solchen Umgebung gibt es eine sogenannte Shell – ein Programm, das textuell bedient wird und mit dem viele essentielle Tätigkeiten, wie das Anlegen und Verschieben von Ordnern, möglich sind. Eine Shell wird in einem sogenannten Terminal-Programm angezeigt, welches das grafische Fenster in Ihrem Betriebssystem darstellt und die Text Ein- und Ausgabe verwaltet. Diese Unterscheidung ist nur manchmal relevant und oft werden beide Namen – Shell und Terminal – gleichwertig benutzt, aber es sollte Ihnen klar sein, dass es einen Unterschied gibt.

Die Befehle, die eine Shell ausführen kann können dabei Bestandteil der Shell sein – eine Shell beherbergt auch eine Programmiersprache – oder sie können andere Programme sein, die eine textuelle Bedienoberfläche haben. `git` ist ein solches Programm, das nicht Kernfunktionalität der Shell ist, sondern von dieser ausgeführt wird.

Eine der Besonderheiten einer Shell ist, dass eingebaute Befehle und Programme gleichwertig miteinander verbunden werden können, sodass komplexe Abläufe durch die Kombination einfacher Befehlen definiert werden können.

In Unix-basierten Betriebssystemen gibt es verschiedene Shell-Programme wie `bash`, `fish` oder `zsh`, welche von der "Ur-Shell" `sh` abstammen und diese erweitern. Unter Windows gibt es die Möglichkeit eine `bash` über das Programm *Git Bash* zu nutzen.

```{margin}
Unter Windows gibt es auch "nativ" ähnliche Programme mit der *Eingabeaufforderung* bzw. der *Power Shell*. Diese unterscheiden sich jedoch teilweise in ihrer Funktionalität und Mächtigkeit und verwenden insbesondere andere Befehle und eine andere Programm-Syntax. Befehle können nicht eins zu eins kopiert werden.
```
## Navigation in der Shell

```{margin}
Je nachdem, welche Shell Sie nutzen, können Sie deren Startkonfiguration mit Dateien wie `.profile`, `.bashrc`, `.zshrc`, … anpassen.Sehen Sie dazu in der Dokumentation Ihrer Shell nach.
```
Wenn Sie eine Shell öffnen dann werden ggf. ein paar Zeilen Text ausgegeben – das hängt von der Konfiguration des Shell-Starts ab. Dann wird der sogenannte Prompt ausgegeben. Dieser kann den aktuellen Ordner o.ä. anzeigen (und kann in der Konfigurationsdatei angepasst werden). Am Ende des Prompts werden oft die zwei Zeichen `$ `&nbsp;angezeigt. Nach der Zeichenkette `$ `&nbsp;geben Sie dann Ihre Befehle ein. In den weiteren Beispielen wird dieses Zeichen genutzt, um Zeilen mit Befehlen von Zeilen mit der Ausgabe der Programme – den Ergebnissen der Befehle – zu unterscheiden.

Nehmen wir für die weiteren Übungen die folgende Ordnerstruktur ({numref}`fig-d-u-ordnerstruktur`) an. Bauen Sie diese bspw. über den Windows Explorer oder den macOS Finder nach, um die Navigation selbst nachzuvollziehen. Die `.md`-Dateien können Sie schon anlegen oder Sie warten, bis Sie gelernt haben, wie Sie in der Shell eine leere Datei anlegen können.

Unter Windows nehmen wir an, dass die Ordner in `C:\Users\Testnutzer\Documents\` liegen. Unter macOS wäre das Äquivalent `/Users/Testnutzer/Documents/`. Denken Sie also immer an Ihr *Dokumentenverzeichnis*, wenn Sie hier `/User/Testnutzer/Documents/` lesen. Unter Linux liegt der Ordner in `/home/Testnutzer/Documents/`. Unter Unix-basierten Betriebssystemen kann dies auch noch abgekürzt geschrieben werden: `~/Documents/`.

```{figure} ../assets/develop/unix/Ordnerstruktur.svg
---
align: left
width: 50%
name: fig-d-u-ordnerstruktur
---
Darstellung der Ordnerstruktur die für die nachfolgenden Beispiele genutzt wird. In einem Ordner `/User/Testnutzer/Documents/Tutorial` liegen zwei Ordner `Markdown` und `Bilder` sowie eine Datei `README.md`. `Bilder` ist leer. `Markdown` enthält wiederum zwei Ordner `01_Technologie` und `02_Didaktik` sowie eine Datei `Einleitung.md`. In `01_Technologie` liegen zwei Dateien `Git.md` und `Github.md`. In `02_Didaktik` liegt eine Datei `Interaktive_Lehrbücher.md`
```

### `pwd` – Print Working Directory
Öffnen Sie ein Terminal. Sie können mit dem Befehl `pwd` herausfinden, in welchem Ordner des Dateisystems Sie sich gerade befinden.
```bash
$ pwd
/Users/Testnutzer/
```
Manche Shell-Prompts haben eingebaut, dass Sie sehen, wo Sie gerade sind. In diesem Fall könnte das so aussehen:
```bash
~ $ 
```
Wenn Sie in einem anderen Ordner wären (bspw. in `/Users/Testnutzer/Documents/Tutorial`), dann könnte das so aussehen:
```bash
~/Documents/Tutorial $ pwd
/Users/Testnutzer/Documents/Tutorial
```

### `cd` – Change Directory
Mit dem Befehl `cd` können Sie den Ordner wechseln, in dem Sie sich befinden. Das geht entweder *absolut* oder *relativ*. Ein absoluter Pfad beginnt in Unix-basierten Systemen immer mit einem `/`. Ein relativer Pfad beginnt nicht mit einem `/` sondern mit einem Ordnernamen oder den speziellen Namen für den aktuellen Ordner `.` oder den übergeordneten Ordner `..`.

`````{admonition} Übung
:class: tip
Nutzen Sie eine absolute Pfadangabe, um in den Ordner `/Users/Testnutzer/Documents/Tutorial` zu wechseln. Beachten Sie dabei, dass Sie den korrekten Nutzernamen verwenden müssen.
````{admonition} Lösung
:class: dropdown
```bash
$ cd /Users/Testnutzer/Documents/Tutorial
```
Um sicherzustellen, dass Sie im richtigen Ordner sind, können Sie `pwd` nutzen.
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial
```
````
`````

### `ls` – LiSt directory contents
Den Inhalt eines Ordners können Sie Sich mit dem Befehl `ls` ausgeben lassen.
```{margin}
Falls Sie die `.md`-Dateien nicht angelegt haben, wird Ihnen hier die `README.md` nicht angezeigt.
```
```bash
$ ls
Bilder
Markdown
README.md
```

Sie können `ls` auch einen Ordnernamen bzw. einen Pfad übergeben wodurch der Inhalt dieses Pfads ausgegeben wird.
`````{admonition} Übung
:class: tip
Welche Ausgaben ergeben die folgenden Befehle?
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial

$ ls

$ ls Bilder

$ ls Markdown

$ cd Markdown; ls ..

$ pwd
```
````{admonition} Lösung
:class: dropdown
Wenn SIe nacheinander die Befehle eingeben sollte Ihr Terminal ungefähr so aussehen:
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial

$ ls
Bilder
Markdown
README.md

$ ls Bilder

$ ls Markdown
01_Technologie
02_Didaktik
Einleitung.md

$ cd Markdown; ls ..
Bilder
Markdown
README.md

$ pwd
/Users/Testnutzer/Documents/Tutorial/Markdown
```
Wenn Sie andere Ergebnisse erhalten haben oder Sie nicht sicher sind, warum diese Ausgabe korrekt ist, dann gehen Sie am besten jeden Befehl noch einmal Schritt für Schritt durch.
````
`````

```{code-cell} ipython3
:tags: [remove_input]
questions = \
[
  { 'question': "Sie befinden Sich im Ordner 02_Didaktik. Wie navigieren Sie in den Ordner Bilder?",
    'type': 'multiple_choice',
    'answers': [
    { 'answer': 'cd Bilder',
      'correct': False,
      'feedback': 'Der Ordner Bilder ist kein Unterordner von 02_Didaktik.'},
    { 'answer': 'cd ../Bilder',
      'correct': False,
      'feedback': 'Der Ordner Bilder liegt nicht neben dem Ordner 02_Didaktik.'},
    { 'answer': 'cd ../../Bilder',
      'correct': True,
      'feedback': 'Richtig!'},
    { 'answer': 'cd ../../../Tutorial/Bilder',
      'correct': True,
      'feedback': "Auch das stimmt. Wir \"gehen\" einen Ordner weiter nach oben und dann wieder zurück in Tutorial."},
    { 'answer': 'cd ~/Documents/Tutorial/Bilder',
      'correct': True,
      'feedback': "Eine absolute Pfadangabe geht jederzeit. Oft sind relative Pfade aber schneller zu tippen und sie funktionieren auch, wenn der Ordner Tutorials an einer anderen Stelle als im Ordner Documents liegt."}
    ]
  },
  { 'question': "Sie befinden Sich im Ordner Tutorial. Wie können Sie Sich den Inhalt von 01_Technologie anzeigen lassen?",
    'type': 'multiple_choice',
    'answers': [
    { 'answer': 'ls 01_Technologie',
      'correct': False,
      'feedback': 'Im Ordner Tutorial gibt es keinen Ordner 01_Technologie.'},
    { 'answer': 'dir Markdown/01_Technologie',
      'correct': False,
      'feedback': 'dir ist der Befehl in Windows. Aber auch dann wäre es falsch, weil dort Backslash benutzt wird. Es müsste dann lauten: dir Markdown\01_Technologie.'},
    { 'answer': 'ls Markdown/01_Technologie',
      'correct': True,
      'feedback': 'Richtig! Das ist die einfachste Variante.'},
    { 'answer': 'cd Markdown; ls 01_Technologie',
      'correct': True,
      'feedback': "Das funktioniert und gibt das richtige Ergebnis aus. Allerdings haben Sie sich dann \"bewegt\" und sind jetzt im Ordner Markdown. Falls Sie das nicht wollen, müssten Sie Sich wieder einen Ordner nach oben bewegen."},
    { 'answer': 'ls -R Markdown',
      'correct': True,
      'feedback': "Sie als Mensch finden so den Inhalt des Ordners 01_Technologie heraus. Allerdings wird Ihnen noch mehr ausgegeben. Wenn Sie die Ausgabe des Befehls mit einem Programm weiterbearbeiten wollten, dann wäre es keine gute Idee, diesen Befehl zu nutzen."}
    ]
  },
]

display_quiz(questions, colors=colors.jupyterquiz)
```

## Arbeiten mit Ordnern und Dateien
Nachdem Sie nun navigieren können wollen wir Ordner und leere Dateien erstellen, sowie diese verschieben, umbenennen und löschen. Dabei lernen Sie auch noch versteckte Dateien und Ordner kennen.
### `mkdir` – MaKe DIRectory
Um einen neuen Ordner anzulegen benutzt man den Befehl `mkdir`. Sie können entweder in den Ordner navigieren, in dem Sie einen Unterordner erstellen wollen, oder Sie können absolute oder relative Pfade nutzen, um den neuen Ordner an der richtigen Stelle zu erstellen.

Wenn Sie im Ordner `Tutorial` sind, dann können Sie einen Ordner `Videos` mit diesem Befehl anlegen:
```bash
$ mkdir Videos
```

`````{admonition} Übung
:class: tip
Legen Sie mit verschiedenen Kombinationen aus Navigation sowie absoluten und relativen Pfaden drei neue Unterordner im Ordner Markdown an. Diese sollen `03_Assessment`, `04_Übungen`, `05_Fazit` lauten. Überprüfen Sie mit `ls`, ob Sie alle Ordner korrekt angelegt haben.

````{admonition} Lösung
:class: dropdown
Mögliche Lösungswege sind:
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial

$ cd Markdown

$ mkdir 03_Assessment
```
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial

$ mkdir Markdown/04_Übungen
```
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial

$ mkdir /Users/Testnutzer/Documents/Tutorial/Markdown/05_Fazit
```

Bonus:
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial

$ cd Markdown/02_Didaktik

$ mkdir ../06_Anhang
```

Überprüfung mit `ls`:
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial

$ ls Markdown
01_Technologie
02_Didaktik
03_Assessment
04_Übungen
05_Fazit
06_Anhang
Einleitung.md
```
````
`````
### `touch` – TOUCH a file
Mit `touch` können Sie eine leere Datei erstellen.
```bash
$ touch LICENSE.md
```
### `mv` – MoVe a file or directory
Erstellen Sie im Ordner `Tutorial` eine Datei mit dem Namen `Multiple_Choice.md`. Mit `mv` können Sie diese nun an die richtige Stelle bewegen:
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial

$ touch Multiple_Choice.md

$ mv Multiple_Choice.md Markdown/03_Assessment/
```
Der Slash (`/`) am Ende des Befehls sagt, dass die Datei *in* den Ordner `03_Assessment` verschoben werden soll. Um sicherzugehen können Sie auch die nachfolgende Pfadangabe nutzen:
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial

$ touch Multiple_Choice.md

$ mv Multiple_Choice.md Markdown/03_Assessment/.
```
Das macht nochmals explizit, dass Sie die Datei *in* den Ordner verschieben.

`mv` wird auch benutzt, um eine Datei umzubenennen.
`````{admonition} Übung
:class: tip
Legen Sie eine Datei mit einem Tippfehler im Namen, bspw. `Kaulsur.md`, und korrigieren Sie dann den Dateinamen.
````{admonition} Lösung
:class: dropdown
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial/Markdown/03_Assessment

$ touch Kaulsur.md

$ mv Kaulsur.md Klausur.md
```

Sie können eine Datei auch gleichzeitig verschieben und umbenennen:
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial/

$ touch Kaulsur.md

$ mv Kaulsur.md Markdown/03_Assessment/Klausur.md
```
````
`````

### `ls -a` – LiSt All files
Erstellen Sie eine Datei mit dem Namen `.hidden` und einen Ordner mit dem Namen `.secrets`. Da beide Namen mit einem `.` beginnen werden sie bei Nutzung von `ls` ohne Kommando-Optionen nicht angezeigt. Um sie anzuzeigen müssen Sie die Option `-a` an den Befehl anhängen.
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial/

$ touch .hidden

$ mkdir .secrets

$ ls
Bilder
Markdown
README.md
Videos

$ ls -a
.
..
.hidden
.secrets
Bilder
Markdown
README.md
Videos
```
Wie Sie sehen beinhaltet der Ordner neben `.hidden` und `.secrets` auch noch die zwei speziellen Ordner `.` und `..`. Wie oben einmal erwähnt steht `.` für den *aktuellen* Ordner und `..` für den *übergeordneten* Ordner.

`````{admonition} Übung
:class: tip
Wenn Sie im Ordner `Markdown` sind, was geben die folgenden Befehle aus? Überlegen Sie zuerst selbst und notieren Sie sich Ihr Ergebnis. Überprüfen Sie dann in der Shell, ob die tatsächlichen Ergebnisse mit Ihren Antworten übereinstimmen.
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial/Markdown

$ ls

$ ls -a

$ ls ..

$ ls ../Markdown/.

$ ls 01_Technologie/../../Bilder/..
```

````{admonition} Lösung
:class: dropdown
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial/Markdown

$ ls
01_Technologie
02_Didaktik
03_Assessment
04_Übungen
05_Fazit
06_Anhang
Einleitung.md

$ ls -a
.
..
01_Technologie
02_Didaktik
03_Assessment
04_Übungen
05_Fazit
06_Anhang
Einleitung.md

$ ls -a ..
.
..
.hidden
.secrets
Bilder
Markdown
README.md
Videos

$ ls ../Markdown/.
01_Technologie
02_Didaktik
03_Assessment
04_Übungen
05_Fazit
06_Anhang
Einleitung.md

$ ls 01_Technologie/../../Bilder/..
Bilder
Markdown
README.md
Videos
```
````
`````

### `rm` – ReMove a file or directory
Wollen Sie eine Datei löschen, so geht das mit `rm`.
```{important}
Wenn Sie eine Datei mit `rm` löschen, dann ist sie endgültig gelöscht und kann nicht wiederhergestellt werden.

Anders als beim Löschen im Windows Explorer oder im macOS Finder gibt es *keinen* Papierkorb.
```
Um einen Ordner zu löschen müssen Sie die Option `-r` nutzen.

```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial/Markdown

$ rm .hidden

$ rm .secrets
rm: .secrets: is a directory

$ ls -a
.
..
.secrets
Bilder
Markdown
README.md
Videos

$ rm -r .secrets

$ ls -a
.
..
Bilder
Markdown
README.md
Videos
```

