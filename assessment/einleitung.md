---
lang: de-DE
---

# Lernstandskontrolle (Assessment) in QUADRIGA OER

QUADRIGA OER sind vorrangig an Selbstlerner\*innen gerichtet, welche ihre Datenkompetenz verbessern wollen. Diese Lernenden benötigen Feedback um einschätzen zu können, wo sie in der Lernerfahrung stehen und wie sie vorankommen, welche nächsten Schritte sie gehen sollten und welche Ziele sie mit der Lernaktivität erreichen können {cite}`hattie2007`. Daher ist das Hauptziel der Lernstandskontrolle in den QUADRIGA OER die Unterstützung der Lernenden während sie OER durcharbeiten. Wir fokussieren uns also auf formatives Selbst-Assessment.

In diesem Kapitel werden zuerst theoretische Überlegungen zu Assessment in Selbstlern-OER vorgestellt. Daraus werden dann Empfehlungen für verschiedene Assessment-Formen für QUADRIGA OER erarbeitet. Anschließend wird die Umsetzung dieser Assessment-Formen in konkreten Technologien innerhalb der Jupyter Books beschrieben. Zuerst wird die Zielgruppe der QUADRIGA OER genauer definiert.

## Zielgruppe von QUADRIGA OER
QUADRGIA entwickelt OER für Wissenschaftler\*innen, die Kompetenzen aus dem Spektrum der Datenkompetenz {cite}`{siehe}neuroth2025` erlernen oder stärken wollen. Genauer sind Wissenschaftler\*innen ab der Qualifikationsstufe der Promovierenden adressiert.

Diesen Lernenden gemein sind Eigenschaften, welche direkten Einfluss auf die Gestaltung der OER und des Assessments darin haben. So sind sie stark selbst-motiviert und besitzen bereits eine gewisse Expertise in ihrer Kerndisziplin. Typischerweise besitzen sie nur vereinzelte und grundlegende Kompetenzen in der Domäne der Datenkompetenzen. Die Zielgruppe lernt viel autodidaktisch oder in kleine Gruppen mit Kolleg\*innen zusammen; durch Lehrpersonal angeleitetes und unterstütztes Lernen findet nur selten statt. Wird in Gruppen gelernt, so ist nicht vorauszusetzen, dass eine der Lernenden die anderen anleiten könnte.

Die OER sind didaktisch für diese Zielgruppe aufbereitet (siehe [Didaktisches Konzept](../struktur_didaktisches_konzept/didaktisches_konzept.md)). Ebenso ist das Assessment auf die Zielgruppe ausgerichtet, was in den nachfolgenden Abschnitten genauer beschrieben wird.

Zusätzlich zur Zielgruppe der Wissenschaftler\*innen können die QUADRIGA OER auch Grundlage für Lehrveranstaltungen bspw. innerhalb eines Studiengangs sein. Dies erfordert jedoch oft eine Umgestaltung von Lernaktivitäten und bspw. eine Einführung von summativem Fremd-Assessment am Ende eines Kurses.

## Assessment ins Selbstlern-OER
Assessment spielt in einer Selbstlern-OER eine besonders wichtige Rolle. 

- Lernende sollen das Assessment zur Selbstkontrolle vor, während und nach der Absolvierung einer OER nutzen können.
- Schnelles, direktes Feedback wird – wo möglich – bevorzugt. Komplexeres Self-Assessment wie bspw. die selbstständige Korrektur der eigenen Abgabe anhand eines Bewertungsrasters wird dennoch an geeigneten Stellen genutzt um der Zielgruppe und deren Kompetenzerwerb gerecht zu werden.
- Assessment vor der Bearbeitung einer OER kann eingesetzt werden, um die individuellen Lernpfade der Lernenden zu unterstützen. Wurde ein Pre-Assessment erfolgreich und ohne großen Aufwand erfolgreich beantwortet, so ist dies ein starkes Indiz, dass die lernende Person die jeweilige OER nicht oder nur zur Wiederholung durcharbeiten muss um die angestrebten Lernziele zu erreichen.

## Assessment-Formen in QUADRIGA OER
In QUADRIGA OER werden vorrangig folgende Assessment-Formate genutzt.
- Single-Choice- / Multiple-Choice-Tests
    Diese Tests sind schnell und einfach in der Korrektur, da diese automatisch erfolgen kann. Die Erstellung muss überlegt durchgeführt werden.
    
    Falsche Antwortmöglichkeiten (Distraktoren) sollten in ihrer Struktur (Länge, Detailgrad) möglichst gleich und inhaltlich plausibel sein.
    Single-Choice-Tests sollten mindestens drei Antwortmöglichkeiten anbieten (1 richtige und 2 falsche). Multiple-Choice-Tests mit n Antwortmöglichkeiten können zwischen 1 und n richtige beinhalten. Eine MC ohne richtige Antwort ist nicht empfohlen, weil sonst das "Nichts-Tun" zu einem korrekten Ergebnis führt.
    
    Jede Frage und deren Antwortmöglichkeiten muss mit einer/mehreren Erklärungen verbunden werden, warum die richtigen Antwortmöglichkeiten richtig und die falschen Antwortmöglichkeiten falsch sind. 
- Elemente in korrekte Reihenfolge bringen
    Dieser Fragetyp eignet sich für die automatische Korrektur.
    
    Gibt es eine natürliche Struktur / einen klaren Prozess, so kann diese(r) durch diesen Fragetyp geprüft werden.
    
    Eine Erklärung für die korrekte Antwort und ggf. schwierige Entscheidungen der Anordnung ist verpflichtend.
- Verknüpfung von Elementen (1:1, 1:n, oder n:m)
    Diese Art von Testfrage kann automatisch korrigiert werden.
    
    Es können verschiedene Beziehungstypen wie Hierarchien, Beinhaltung, Gegensätze, … geprüft werden. Typischerweise bauen diese Fragen auf einer bi-partiten Gruppe von Elementen auf, wobei ein Element der "linken" Gruppe mit einem oder mehreren Elementen der "rechten" Gruppe verknüpft werden sollen. Es besteht die Möglichkeit, dass nicht alle Elemente der "rechten" Gruppe verknüpft werden müssen. Typischerweise müssen alle Elemente der "linken" Gruppe mindestens einmal verknüpft werden.
    Vorgesehener Beziehungstyp und die Anzahl der möglichen Verknüpfungen müssen in der Frage definiert werden.
    
    Dieser Fragentyp kann auch in Form eines Lückentextes dargestellt werden.
    
    Eine Erklärung, warum eine Elementverknüpfung korrekt ist und die anderen Varianten nicht ist verpflichtend.
- Tests auf ein festgelegtes, nach Vorgaben formatiertes Ergebnis
    Dieser Test kann ggf. automatisch korrigiert werden, wenn das Ergebnis eineindeutig ist.
    
    Typischerweise hat dieser Test Zahlen oder einzelne Wörter als korrekte Antwort. Ggf. können Fehlerbereiche wie ±1% oder Unterschiede in der Groß-/Kleinschreibung automatisch berücksichtigt werden.
    
    Schwierig ist dieser Fragetyp, wenn mehrere Antworten korrekt sein können. In einem gewissen Rahmen ist dies modellierbar, aber ab einer gewissen Komplexität der möglichen korrekten Antworten ist dieser Fragetyp nicht mehr nutzbar.
    
    Dieser Fragentyp kann auch in der Form eines Lückentextes dargestellt werden.
    
    Eine Erklärung nicht nur der korrekten Antwort, sondern auch von "Fehlerbereichen" mit Hinweisen auf die korrekte Antwort ist verpflichtend.

- Programmierung einer Funktion mit festgelegtem Interface
    Dieser Fragetyp kann ggf. mit (vorgegebenen und ggf. geheimen) Testfunktionen automatisch überprüft werden.
    
    Diese Art der Aufgabe fordert zwingend, dass die vorgegebenen Testfunktionen nützliche Hinweise zur Korrektur der eigenen Funktion liefern. Dieser Aufgabentyp funktioniert nur, wenn Lernende beliebig oft die Testfunktionen auf ihre Antwort-Funktion anwenden können.
    
    Es müssen nicht zwingend gesonderten, geheimen Testfunktionen zur Überprüfung einer "Abgabe" existieren.
- Programmierung/Konfiguration einer Datenverarbeitungs-Pipeline
    Ähnlich zum Fragentyp der Programmierung einer Funktion kann auch dieser Fragentyp ggf. automatisch korrigiert werden, solange ein Eingabedatensatz und Test-Funktionen sowie ggf. ein Ausgabedatensatz existieren.
    Für die Bearbeitung müssen zusätzlich mindestens ein Test-Eingabedatensatz und offengelegte Test-Funktionen sowie ggf. mindestens ein Test-Ausgabedatensatz existieren, anhand derer die Lernenden ihre Datenverarbeitungs-Pipeline entwickeln und testen können.
    
    Diese Art der Aufgabe fordert zwingend, dass die vorgegebenen Testfunktionen nützliche Hinweise zur Korrektur der eigenen Funktion liefern. Dieser Aufgabentyp funktioniert nur, wenn Lernende beliebig oft die Testfunktionen auf ihre Antwort-Funktion anwenden können.
    
    Es müssen nicht zwingend gesonderten, geheimen Testfunktionen zur Überprüfung einer "Abgabe" existieren.
- Self-Assessment-Aufgaben
    Diese Gruppe von Fragen wird durch die Lernenden selbst bewertet. Dazu erhalten Sie (nach Abgabe ihrer Antwort) eine Kombination aus Musterlösung(en) und/oder Bewertungskriterien sowie Anleitung, wie sie diese anwenden sollen. Alle Bewertungs-Informationen können auch mit der Aufgabenstellung bekanntgegeben werden.
    
    Diese Art der Aufgabe verlässt sich auf die Selbstreflexion der Lernenden. Eine Abwandlung als Peer-Review ist ggf. möglich, wenn mehrere Lernende gleichzeitig die Aufgabe bearbeiten (siehe bspw. MOOCs) oder wenn es eine Lehrperson gibt. Dies ist im Rahmen von QUADRIGA nicht explizit vorgesehen.
    
    Eine Bewertung/ein Feedback durch ein mit Aufgabenstellung, Musterlösungen und Bewertungskriterien trainiertes LLM-System ist denkbar. Die Nützlichkeit und Validität eines solchen Feedbacks müssen noch überprüft werden.
    
    Dieser Fragetyp wird angewendet für komplexe Fragen, die sich nicht oder nicht einfach/fehlerfrei durch die anderen Fragetypen abbilden lassen. Dies betrifft vor allem Aufgaben der selbstständigen Erschaffung von Code, Text, Graphiken, …. Dies erfordert die Produktion von Wissen/Information und nicht "nur" die Erkennung von korrekten Antworten oder das In-Beziehung-Setzen von vorgegebener Information.

Eine Möglichkeit, die Produktion von Wissen zu testen ist, die Lernenden zuerst auf eine Frage selbst eine Antwort formulieren zu lassen und dann (auf einer nächsten Seite) diese bspw. 3 vorformulierten Antwortmöglichkeiten gegenüberzustellen, aus denen dann eine korrekte auswählt werden muss. Die Lernenden müssen so zuerst eine Antwort selbst generieren und können dann ihre – richtige oder falsche – Antwort mit drei Antwortmöglichkeiten vergleichen und ggf. auf Basis der darin „versteckten“ Hinweise verbessern. Die Auswahl der richtigen Antwortmöglichkeit ist dann ein zusätzlicher Verifikationsschritt, bei dem die Lernenden entweder in Ihrer eigenen Antwort und/oder der gewählten Antwortmöglichkeit bestätigt werden, oder indem Sie eine Antwortmöglichkeit als gesichert falsch eliminieren, um auf Basis dieser neuen Informationen nochmals ihre selbst-formulierte Antwort verbessern und/oder die korrekte Antwort aus den restlichen Antwortmöglichkeiten auswählen können. Wie immer gilt, dass falsche Antwortmöglichkeiten möglichst eine Begründung beinhalten sollten, die die Lernenden unterstützt in der Herausarbeitung der richtigen Antwort(möglichkeit).

Portfolios wären schön, sind aber technisch nicht wirklich umsetzbar, weil keine Lehrkapazität für die Kurse veranschlagt ist.

### Eignung von Assessment-Methoden für gewisse Lernziele
Wie bei den Fragetypen angedeutet haben diese Eigenschaften, die sich auf die überprüfbaren Inhalte/Lernziele auswirken.
Erkennen, Verstehen und ggf. Anwenden (siehe Bloom, Schermutzki) können mit den ersten, einfacheren Fragetypen überprüft werden. Anwenden und Analysieren lassen sich ggf. noch automatisch korrigieren, wenn die Frage/Aufgabenstellung eng genug definiert ist. Spätestens, wenn es um das Beurteilen und Gestalten geht, sind diese vorrangig nur noch durch komplexe Aufgaben – im Kontext von QUADRIGA durch Self-Assessment – zu überprüfen.
Bei affektiven Lernzielen ergibt sich ein ähnliches Bild, sodass die ersten Stufen (siehe Bloom, Schüller) noch durch die ersten Fragetypen abgedeckt werden können während höhere Stufen vorrangig durch komplexe Aufgaben – hier Self-Assessment – überprüft werden müssen.

### Auswahl der Assessment-Inhalte
Die im Assessment zu überprüfenden Inhalte der OER ergeben sich aus den Lernzielen und der Zielgruppe der OER.

Die Lernziele definieren die "obere" Grenze, die Zielgruppe definiert die "untere" Grenze. Zudem ist der Weg von Vorwissen/Grundlagenwissen bzw. -fähigkeiten der Zielgruppe zum Lernziel zu beachten.

Welche "Zwischenschritte" sind für den Lernerfolg essentiell? Welche sind "nur" Wiederholung?

Das Assessment kann durch Inhalt und Struktur auch bei der Erlangung der Lernziele unterstützen. Bei Pre-Assessment gesetzte Schwerpunkte suggerieren Wichtigkeit der Inhalte bei Lernenden. Assessment während der OER und Post-Assessment steuern ggf. die Wiederholung gewisser Inhalte.


### Assessment und GenAI
Es wird bei jedem Assessment festgelegt, ob und in wie weit eine Unterstützung durch Generative-AI-Systeme durch Lernende eingeplant ist. Folgen die Lernenden diesen Empfehlungen nicht, so sind die Ergebnisse des Assessments nicht aussagekräftig. Die Lernenden sind selbst in der Verantwortung, die Assessments richtig anzuwenden. Wird die OER wie oben besprochen in einer formalen Lehrsituation genutzt, so müssen ggf. die Lehrenden auf die Einhaltung der Vorgaben achten.

## Technologien für die Umsetzung des Assessments
Informationen zur Umsetzung von Quizzes mit JupyterQuiz finden Sie auf der [entsprechenden Unterseite](./jupyterquiz.ipynb).

Informationen zur Umsetzung von Test-Driven Assessment finden Sie auf der [entsprechenden Unterseite](./test-driven_assessment.ipynb).


# Literatur
```{bibliography}
:filter: docname in docnames
```
