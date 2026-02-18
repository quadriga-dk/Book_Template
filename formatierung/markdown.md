(formatierung:markdown)=

# Markdown Dateien

Markdown ist <a href="https://daringfireball.net/projects/markdown/"
    target="_blank" class="external-link">ursprünglich</a> eine
leichtgewichtige Auszeichnungssprache welche auch in der reinen
Text-Darstellung (bspw. in einem Texteditor) gut gelesen (und geschrieben)
werden kann.

Nachfolgend werden wir zuerst auf grundlegende, klassische Markdown-Syntax
eingehen und danach auf die Erweiterungen, die MyST-Markdown ermöglicht,
eingehen.

## Markdown 101

### Text

Text, den sie in einer Markdown-Datei schreiben wird normalerweise direkt als
Text ausgegeben.

Um einen neuen Absatz zu beginnen muss in der Datei eine Leerzeile eingefügt
sein. Dies erlaubt es, auch die Textansicht zu formatieren, ohne
unbeabsichtigte Zeilenumbrüche im gerenderten Resultat zu generieren. Öffnen
Sie als Beispiel auch die dieser Seite zugrunde liegende Datei
({download}`markdown.md`).

### Überschriften

Da Markdown von Anfang an HTML als Zielrepräsentation vorsah gibt es sechs
Überschrift-Ebenen. Für manche dieser Ebenen gibt es mehrere Syntaxvarianten,
jedoch hat sich klar die Nutzung von `#` für Überschriften durchgesetzt. Eine
Überschrift ist eine Zeile, welche mit mindestens einem `#` gefolgt von einem
Leerzeichen beginnt. Die Anzahl der `#` entspricht der hierarchischen Ordnung
und wird direkt auf `<h1>` bis `<h6>` in HTML übertragen.

```markdown
# H1 Überschrift

## H2 Überschrift

### H3 Überschrift

#### H4 Überschrift

##### H5 Überschrift

###### H6 Überschrift
```

Typischerweise gibt es pro Datei nur eine Überschrift auf oberster Ebene (`# `
entsprechend `<h1>` in HTML) und es sollten keine Überschrift-Stufen
übersprungen werden.

### Links

Links können entweder direkt, mit `<` und `>` geklammert, eingefügt werden,
oder Sie nutzen die Markdown-Link-Syntax.

- Direkte Einbettung:

    ```markdown
    <https://quadriga-dk.github.io/Book_Template/>
    ```

    führt zu:

    <https://quadriga-dk.github.io/Book_Template/>

- Markdown-Link-Syntax:

    ```markdown
    [Book_Template](https://quadriga-dk.github.io/Book_Template/)
    ```

    führt zu:

    [Book_Template](https://quadriga-dk.github.io/Book_Template/)

In QUADRIGA nutzen wir für Links zu externen Seiten eine etwas [andere
Formatierung (in HTML-Syntax)](./link_in_neuem_tab.md).

### Auflistungen

Markdown hat Syntax für Aufzählungslisten (nummeriert und nicht nummeriert).
Für nicht nummerierte Listen können verschiedene "Gedankenstriche" genutzt
werden wie `-`, `*` und `+`. Nummerierte Listen bestehen aus einer Zahl und
einem `.`. Die Zahlen können dabei aufsteigend sein, müssen es aber nicht.

```
- Eins
    + zwei
    + drei
- vier
    * fünf
        * sechs
```

- Eins
    - zwei
    - drei
- vier
    - fünf
        - sechs

```
1. Eins
    1. zwei
    2. drei
1. vier
    1. fünf
        1. sechs
```

1. Eins
    1. zwei
    2. drei
1. vier
    1. fünf
        1. sechs

### Code-Blöcke

Wollen Sie Code darstellen oder auch nur unformatierten Text in
Festbreitenschrift, so geht dies mit der folgenden Syntax.

````markdown
```python
2 + 3
```
````

```python
2 + 3
```

Direkt nach den drei `` ` `` kann eine Programmiersprache oder ein
Dateiformat angegeben werden. Dieser Bezeichner wird bei der Umwandlung bspw.
in HTML an ein Programm übergeben, welches den Codeblock entsprechend mit
Syntax-Hervorhebungen darstellt.

Wollen Sie einzelne Wörter oder Phrasen innerhalb eines Satzes als Code
formatieren, so geht dies mit einzelnen `` ` `` als "Klammern".

```
Normaler Text gefolgt in dem eine `Code Phrase` eingebettet ist.
```

Normaler Text gefolgt in dem eine `Code Phrase` eingebettet ist.

### Text kursiv und fett setzen

Wollen Sie Text _kursiv_ oder **fett** setzen, so ist dies ebenfalls möglich.

```
_kursiv_ oder *kursiv*
```

_kursiv_ oder _kursiv_

```
__fett__ oder **fett**
```

**fett** oder **fett**

Viele Editoren favorisieren `_` für kursiv und `**` für fett, sodass die
Unterscheidung beim Lesen im Texteditor leichter fällt.

### HTML

In Markdown können wann immer nötig auch HTML-Tags genutzt werden. Besonders
hilfreich sind diese, wenn ein Zeilenumbruch (`<br>`) ohne neuen Absatz, ein
Link mit spezifischen Parametern oder auch eine komplexe Tabelle eingefügt
werden soll. Selbst wenn Markdown-Dialekte mit größerem Funktionsumfang wie
MyST genutzt werden ist die Nutzung von HTML teilweise nötig um einen
gewünschten Effekt zu erzielen.

## MyST

MyST-Markdown führt vor allem zwei Funktionalitäten ein: _roles_ und
_directives_. Eine _role_ ist die Erweiterung von der Code-Auszeichnung im
Fließtext (einzelne `` ` `` als "Klammern") und ein _directive_ ist ein
abgewandelter Code-Block.

**role**:

```
{role}`Wort oder Phrase`
```

**directive**:

````
```{directive}
Mehrzeiliger Text,
der besonders
         verarbeitet
   wird
```
````

Beim Schreiben von OER mit Jupyter Book werden Sie vor allem zwei dieser
Erweiterungen nutzen: Admonitions und Zitationen.

### Admonitions

Admonitions sind Textblöcke (_directive_), die graphisch und farblich gegenüber
dem restlichen Text hervorgehoben werden. Mehr Details zu den speziellen
Varianten für QUADRIGA OER finden Sie im [Abschnitt zu
Admonitions](/formatierung/admonitions.md).

````
```{admonition} Test-Lernziel
:class: lernziel

Das ist ein Test-Lernziel
```
````

```{admonition} Test-Lernziel
:class: lernziele

Das ist ein Test-Lernziel
```

### Zitationen

Zitieren ist über mehrere _role_-Varianten möglich. Die Grundform `` {cite}`neuroth2025` ``
wird folgendermaßen dargestellt: {cite}`neuroth2025`.

Damit dies funktioniert muss der sog. citekey in der Bibliographie verfügbar
sein. In QUADRIGA nutzen wir dafür immer die Datei `references.bib` im
Wurzelverzeichnis des Jupyter Book, welche über die Definition in `_config.yml`
festgelegt wurde.
