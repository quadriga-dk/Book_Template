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
---
```{code-cell} ipython3
:tags: [remove_cell]
from jupyterquiz import display_quiz
```
# Unix

Viele der Kommandozeilenbefehle, die hier in dieser Anleitung genutzt werden, gehen von einer Unix-Umgebung aus. In einer solchen Umgebung gibt es eine sogenannte Shell – ein Programm, das textuell bedient wird und mit dem viele essentielle Tätigkeiten wie das Anlegen und Verschieben von Ordnern möglich sind. Eine Shell wird in einem sogenannten Terminal-Programm angezeigt, welches das grafische Fenster in Ihrem Betriebssystem zeichnet und die Text Ein- und Ausgabe verwaltet. Diese Unterscheidung ist nur manchmal relevant und oft werden beide Namen – Shell und Terminal – gleichwertig benutzt, aber es sollte Dir klar sein, dass es einen Unterschied gibt.

Die Befehle, die eine Shell ausführen kann können dabei Bestandteil der Shell sein – eine Shell beherbergt auch eine Programmiersprache – oder sie können andere Programme sein, die eine textuelle Bedienoberfläche haben. `git` ist ein solches Programm, das nicht Kernfunktionalität der Shell ist sondern von dieser ausgeführt wird.

Eine der Besonderheiten einer Shell ist, dass eingebaute Befehle und Programme gleichwertig miteinander verbunden werden können, sodass komplexe Abläufe mit einfachen Befehlen ausgeführt werden können.

In Unix-basierten Betriebssystemen gibt es verschiedene Shell-Programme wie `bash`, `fish` oder `zsh`, welche von der "Ur-Shell" `sh` abstammen und diese erweitern. Unter Windows gibt es die Möglichkeit eine `bash` über das Programm *Git Bash* zu nutzen.

```{margin}
Unter Windows gibt es auch "nativ" ähnliche Programme mit der *Eingabeaufforderung* bzw. der *Power Shell*. Diese unterscheiden sich jedoch teilweise in ihrer Funktionalität und Mächtigkeit und verwenden andere Befehle und eine andere Programm-Syntax.
```
## Navigation in der Shell

```{margin}
Je nachdem, welche Shell Du benutzt kannst Du die Startkonfiguration anpassen über Dateien wie `.profile`, `.bashrc`, `.zshrc`, … Sieh Dir dazu die Dokumentation deiner Shell an.
```
Wenn die Shell öffnet werden ggf. ein paar Zeilen Text ausgegeben – das hängt von der Konfiguration des Shell-Starts ab. Dann wird der sogenannte Prompt ausgegeben. Dieser kann den aktuellen Ordner o.ä. anzeigen (und kann in der Konfigurationsdatei angepasst werden). Am Ende des Prompts wird oft die Zeichen `$ `&nbsp;angezeigt. Nach der Zeichenkette `$ `&nbsp;gibtst Du dann deine Befehle ein. In den weiteren Beispielen wird dieses Zeichen genutzt, um Zeilen mit Befehlen von Zeilen mit der Ausgabe der Programme, den Ergebnissen der Befehle, zu unterscheiden.

Nehmen wir für die weiteren Übungen die folgende Ordnerstruktur ({numref}`fig-d-u-ordnerstruktur`) an. Baue diese bspw. über den Windows Explorer oder den macOS Finder nach, um die Navigation selbst nachzuvollziehen. Die `.md`-Dateien kannst Du schon anlegen oder Du wartest, bis Du gelernt hast, wie Du in der Shell eine leere Datei anlegen kannst.

Unter Windows nehmen wir an, dass die Ordner in `C:\Users\Testnutzer\Documents\` liegen. Unter macOS wäre das Äquivalent `/Users/Testnutzer/Documents/`. Denke Dir also immer Dein *Dokumentenverzeichnis*, wenn Du hier `/User/Testnutzer/Documents/` liest. Unter Linux liegt der Ordner in `/home/Testnutzer/Documents/`. Unter Unix-basierten Betriebssystemen kann dies auch noch abgekürzt geschrieben werden: `~/Documents/`.

```{figure} ../assets/develop/unix/Ordnerstruktur.svg
---
align: left
width: 50%
name: fig-d-u-ordnerstruktur
---
Darstellung der Ordnerstruktur die für die nachfolgenden Beispiele genutzt wird. In einem Ordner `/User/Testnutzer/Documents/Tutorial` liegen zwei Ordner `Markdown` und `Bilder` sowie eine Datei `README.md`. `Bilder` ist leer. `Markdown` enthält wiederum zwei Ordner `01_Technologie` und `02_Didaktik` sowie eine Datei `Einleitung.md`. In `01_Technologie` liegen zwei Dateien `Git.md` und `Github.md`. In `02_Didaktik` liegt eine Datei `Interaktive_Lehrbücher.md`
```

### `pwd` – Print Working Directory
Öffne ein Terminal. Du kannst mit dem Befehl `pwd` herausfinden, in welchem Ordner Du gerade bist.
```bash
$ pwd
/Users/Testnutzer/
```
Manche Shell-Prompts haben eingebaut, dass Du siehst, wo Du gerade bist. In diesem Fall könnte das so aussehen:
```bash
~ $ 
```
Wenn Du in einem anderen Ordner wärst (bspw. in `/Users/Testnutzer/Documents/Tutorial`), dann könnte das so aussehen:
```bash
~/Documents/Tutorial $ pwd
/Users/Testnutzer/Documents/Tutorial
```

### `cd` – Change Directory
Mit dem Befehl `cd` kannst Du den Ordner wechseln, in dem Du bist. Das geht einmal *absolut* und einmal *relativ*. Ein absoluter Pfad beginnt in Unix-basierten Systemen immer mit einem `/`. Ein relativer Pfad beginnt nicht mit einem `/` sondern mit einem Ordnernamen oder den speziellen Namen für den aktuellen Ordner `.` oder den übergeordneten Ordner `..`.

`````{admonition} Übung
:class: tip
Nutze einen absoluten Pfad, um in den Ordner `/Users/Testnutzer/Documents/Tutorial` zu wechseln. Beachte, dass Du den korrekten Nutzernamen verwendest.
````{admonition} Lösung
:class: dropdown
```bash
$ cd /Users/Testnutzer/Documents/Tutorial
```
Um sicherzustellen, dass Du im richtigen Ordner bist kannst Du `pwd` nutzen.
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial
```
````
`````
### `ls` – LiSt directory contents
Den Inhalt eines Ordners kannst Du Dir mit dem Befehl `ls` ausgeben lassen.
```{margin}
Falls Du die `.md`-Dateien nicht angelegt hast wird Dir hier die `README.md` nicht angezeigt.
```
```bash
$ ls
Bilder
Markdown
README.md
```

Du kannst `ls` auch einen Ordnernamen bzw. einen Pfad übergeben und es wird der Inhalt dieses Pfads ausgegeben.
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
Wenn Du nacheinander die Befehle eingibst sollte Dein Terminal ungefähr so aussehen:
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
Wenn Du andere Ergebnisse hast oder Dir nicht sicher bist, warum diese Ausgabe korrekt ist, dann gehe jeden Befehl noch einmal Schritt für Schritt durch.
````
`````

```{code-cell} ipython3
:tags: [remove_input]
questions = \
[
  { 'question': "Du befindest Dich im Ordner 02_Didaktik. Wie navigierst Du in den Ordner Bilder?",
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
      'feedback': "Eine absolute Pfadangabe geht jederzeit. Oft sind relative Pfade aber schneller zu tippen und sie funktionieren auch, wenn der Ordner Tutorials an einer anderen Stelle als in Documents liegt."}
    ]
  },
  { 'question': "Du befindest Dich im Ordner Tutorial. Wie kannst Du Dir den Inhalt von 01_Technologie anzeigen lassen?",
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
      'feedback': "Das funktioniert und gibt das richtige Ergebnis aus. Allerdings hast Du Dich \"bewegt\" und bist jetzt im Ordner Markdown. Falls Du das nicht willst, müsstest Du wieder einen Ordner nach oben."},
    { 'answer': 'ls -R Markdown',
      'correct': True,
      'feedback': "Du als Mensch bekommst so den Inhalt des Ordners 01_Technologie heraus. Allerdings wird Dir noch mehr ausgegeben. Wenn Du die Ausgabe des Befehls mit einem Programm weiterbearbeiten wolltest, dann wäre es keine gute Idee, diesen Befehl zu nutzen."}
    ]
  },
]

display_quiz(questions)
```

## Arbeiten mit Ordnern und Dateien
Nachdem Du nun navigieren kannst wollen wir Ordner und leere Dateien erstellen sowie diese verschieben, umbenennen und löschen. Dabei lernen wir auch noch versteckte Dateien und Ordner kennen.
### `mkdir` – MaKe DIRectory
Um einen neuen Ordner anzulegen benutzt man den Befehl `mkdir`. Du kannst entweder in den Ordner navigieren, in dem Du einen Unterordner erstellen willst, oder Du kannst absolute oder relative Pfade nutzen, um den neuen Ordner an der richtigen Stelle zu erstellen.

Wenn Du im Ordner `Tutorial` bist, dann kannst Du einen Ordner `Videos` mit diesem Befehl anlegen:
```bash
$ mkdir Videos
```

`````{admonition} Übung
:class: tip
Lege mit verschiedenen Kombinationen aus Navigation und absoluten und relativen Pfaden drei neue Unterordner im Ordner Markdown an. Diese sollen `03_Assessment`, `04_Übungen`, `05_Fazit` lauten. Überprüfe mit `ls`, ob Du alle Ordner korrekt angelegt hast.

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
Mit `touch` kannst Du eine leere Datei erstellen.
```bash
$ touch LICENSE.md
```
### `mv` – MoVe a file or directory
Erstelle im Ordner `Tutorial` eine Datei mit dem Namen `Multiple_Choice.md`. Mit `mv` kannst Du diese nun an die richtige Stelle bewegen:
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial

$ touch Multiple_Choice.md

$ mv Multiple_Choice.md Markdown/03_Assessment/
```
Der Slash (`/`) am Ende des Befehls sagt, dass die Datei *in* den Ordner `03_Assessment` verschoben werden soll. Um sicherzugehen kannst Du auch die nachfolgende Pfadangabe machen:
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial

$ touch Multiple_Choice.md

$ mv Multiple_Choice.md Markdown/03_Assessment/.
```
Das macht nochmals explizit, dass Du die Datei *in* den Ordner verschiebst.

`mv` wird auch benutzt, um eine Datei umzubenennen.
`````{admonition} Übung
:class: tip
Lege eine Datei mit einem Tippfehler im Namen, bspw. `Kaulsur.md`, und nenne sie dann um.
````{admonition} Lösung
:class: dropdown
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial/Markdown/03_Assessment

$ touch Kaulsur.md

$ mv Kaulsur.md Klausur.md
```

Du kannst eine Datei auch gleichzeitig verschieben und umbenennen:
```bash
$ pwd
/Users/Testnutzer/Documents/Tutorial/

$ touch Kaulsur.md

$ mv Kaulsur.md Markdown/03_Assessment/Klausur.md
```
````
`````

### `ls -a` – LiSt All files
Erstelle eine Datei mit dem Namen `.hidden` und einen Ordner mit dem Namen `.secrets`. Da sie mit einem `.` beginnen werden sie bei Nutzung von `ls` ohne Kommando-Optionen nicht angezeigt. Um sie anzuzeigen musst Du die Option `-a` an den Befehl anhängen.
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
Wie Du siehst beinhaltet der Ordner neben `.hidden` und `.secrets` auch noch die zwei speziellen Ordner `.` und `..`. Wie oben einmal erwähnt steht `.` für den *aktuellen* Ordner und `..` für den *übergeordneten* Ordner.

`````{admonition} Übung
:class: tip
Wenn Du im Ordner `Markdown` bist, was geben die folgenden Befehle aus?
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
Willst Du eine Datei löschen, so geht das mit `rm`.
```{important}
Wenn Du eine Datei mit `rm` löschst, dann ist sie endgültig gelöscht und kann nicht wiederhergestellt werden.

Anders als beim Löschen im Windows Explorer oder im macOS Finder gibt es *keinen* Papierkorb.
```
Um einen Ordner zu löschen musst Du die Option `-r` nutzen.

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

