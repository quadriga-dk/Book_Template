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
# Exkurs: Unix

Viele der Kommandozeilenbefehle, die hier in dieser Anleitung genutzt werden, gehen von einer Unix-Umgebung aus. In einer solchen Umgebung gibt es eine sogenannte Shell – ein Programm, das textuell bedient wird und mit dem viele essentielle Tätigkeiten wie das Anlegen und Verschieben von Ordnern möglich sind. Eine Shell wird in einem sogenannten Terminal-Programm angezeigt, welches das grafische Fenster in Ihrem Betriebssystem zeichnet und die Text Ein- und Ausgabe verwaltet. Diese Unterscheidung ist nur manchmal relevant, sollte aber einmal genannt werden.

Die Befehle, die eine Shell ausführen kann können dabei Bestandteil der Shell sein – eine Shell beherbergt auch eine Programmiersprache – oder sie können andere Programme sein, die eine textuelle Bedienoberfläche haben. `git` ist ein solches Programm, das nicht Kernfunktionalität der Shell ist sondern von dieser ausgeführt wird.

Eine der Besonderheiten einer Shell ist, dass eingebaute Befehle und Programme gleichwertig miteinander verbunden werden können, sodass komplexe Abläufe mit einfachen Befehlen ausgeführt werden können.

In Unix-basierten Betriebssystemen gibt es verschiedene Shell-Programme wie `bash`, `fish` oder `zsh`, welche von der "Ur-Shell" `sh` abstammen und diese erweitern. Unter Windows gibt es die Möglichkeit eine `bash` über das Programm *Git Bash* zu nutzen.
```{margin}
Unter Windows gibt es auch "nativ" ähnliche Programme mit der *Eingabeaufforderung* bzw. der *Power Shell*. Diese unterscheiden sich jedoch teilweise in ihrer Funktionalität und Mächtigkeit und verwenden andere Befehle und eine andere Programm-Syntax.
```
## Navigation in der Shell
```{margin}
Je nachdem, welche Shell Du benutzt kannst du die Startkonfiguration anpassen über Dateien wie `.profile`, `.bashrc`, `.zshrc`, … Sieh Dir dazu die Dokumentation deiner Shell an.
```
Wenn die Shell öffnet werden ggf. ein paar Zeilen Text ausgegeben – das hängt von der Konfiguration des Shell-Starts ab. Dann wird der sogenannte Prompt ausgegeben. Dieser kann den aktuellen Ordner o.ä. anzeigen (und kann in der Konfigurationsdatei angepasst werden). Am Ende des Prompts wird oft das Zeichen `$` angezeigt. Nach dem `$` gibtst Du dann deine Befehle ein. In den weiteren Beispielen wird dieses Zeichen genutzt, um Zeilen mit Befehlen von Zeilen mit der Ausgabe der Programme, den Ergebnissen der Befehle, zu unterscheiden.

Nehmen wir für die weiteren Übungen die folgende Ordnerstruktur ({numref}`fig-d-u-ordnerstruktur`) an. Wenn Du willst kannst du diese bspw. über den Windows Explorer oder den macOS Finder anlegen, die Navigation selbst nachzuvollziehen. Unter Windows nehmen wir an, dass die Ordner in `C:\Users\Testnutzer\Documents\` liegen. Unter macOS wäre das Äquivalent `/Users/Testnutzer/Documents/`. Denke Dir also immer dein *Dokumentenverzeichnis*, wenn du hier `/User/Testnutzer/Documents/` liest. Unter Unix-basierten Betriebssystemen kann dies auch noch abgekürzt geschrieben werden: `~/Documents/`.

```{figure} ../assets/develop/unix/Ordnerstruktur.svg
---
align: left
width: 50%
name: fig-d-u-ordnerstruktur
---
Darstellung der Ordnerstruktur die für die nachfolgenden Beispiele genutzt wird. In einem Ordner `/User/Testnutzer/Documents/Tutorial` liegen zwei Ordner `Markdown` und `Bilder` sowie eine Datei `README.md`. `Bilder` ist leer. `Markdown` enthält wiederum zwei Ordner `01_Technologie` und `02_Didaktik` sowie eine Datei `Einleitung.md`. In `01_Technologie` liegen zwei Dateien `Git.md` und `Github.md`. In `02_Didaktik` liegt eine Datei `Interaktive_Lehrbücher.md`
```


- `pwd`
- `cd`
- `ls`
- …


```{code-cell} ipython3
:tags: [remove_input]
questions = \
[
  { 'question': "Du befindest dich im Ordner 02_Didaktik. Wie navigierst Du in den Ordner Bilder?",
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
  { 'question': "Du befindest dich im Ordner Tutorial. Wie kannst Du Dir den Inhalt von 01_Technologie anzeigen lassen?",
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
      'feedback': "Das funktioniert und gibt das richtige Ergebnis aus. Allerdings hast Du Dich \"bewegt\" und bist jetzt im Ordner Markdown. Falls du das nicht willst, müsstest du wieder einen Ordner nach oben."},
    { 'answer': 'ls -R Markdown',
      'correct': True,
      'feedback': "Du als Mensch bekommst so den Inhalt des Ordners 01_Technologie heraus. Allerdings wird Dir noch mehr ausgegeben. Wenn Du die Ausgabe des Befehls mit einem Programm weiterbearbeiten wolltest, dann wäre es keine gute Idee, diesen Befehl zu nutzen."}
    ]
  },
]

display_quiz(questions)
```

## Arbeiten mit Ordnern
- `mkdir`
- `mv`
  - auch mit Dateien
- `ls -lah`
- …


