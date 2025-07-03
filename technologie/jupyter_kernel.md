---
lang: de-DE
---

(jupyter_kernel)=
# Jupyter Kernels

Jupyter Kernels sind Programm-Umgebungen, die ein Jupyter Notebook interaktiv werden lässt. Die korrekte Konfiguration des Kernels ist für die Lokale Entwicklung ebenso wie für die Nutzung in GitHub Actions (und anderen CI/CD-Umgebungen) relevant.

```{admonition} Was ist ein Jupyter Kernel?
:class: hinweis

Ein Jupyter Kernel ist ein separater Prozess, der Ihren Code ausführt und mit der Jupyter-Benutzeroberfläche kommuniziert. Wenn Sie Code in Ihrem Buch schreiben, nimmt der Kernel Ihren Code entgegen, führt ihn in der entsprechenden Programmiersprache aus und liefert die Ergebnisse zurück.
```

## Grundlagen und Funktionsweise

Jupyter Notebooks können mit vielen verschiedenen Programmiersprachen arbeiten – Python, R, Julia, Scala und auch spezialisierten Sprachen wie SPARQL für Datenbankabfragen. Jede Sprache benötigt ihre eigene Ausführungsumgebung, um den Code korrekt zu verarbeiten. Deshalb brauchen wir verschiedene Kernels für verschiedene Sprachen.

Ohne Kernels,
- würde Ihr Code nicht ausgeführt
- würden Variablen nicht zwischen Zellen gespeichert und
- könnten Sie keine Ausgaben, Diagramme oder Ergebnisse sehen.

Die am häufigsten verwendeten Kernels in unseren Jupyter Books sind der *IPython Kernel* für Python-Code, der *IR Kernel* für R-Code und der *SPARQL Kernel* für Datenbankabfragen mit der SPARQL-Abfragesprache zur Arbeit mit Wissensgraphen und semantischen Daten.

## Kernels in GitHub Actions einrichten

Wenn Sie Ihr Jupyter Book lokal erstellen müssen Sie auch die passenden Kernels lokal installieren. Der Python-Kernel wird bei einer Installation des Pakets `jupyter` mitinstalliert. Andere Kernels müssen Sie ggf. selbst nachinstallieren. Befolgen Sie dazu die Anweisungen im jeweiligen Book bzw. orientieren Sie sich an den Nachfolgenden ausführungen. Eine GitHub Action startet normalerweise mit einer leeren Linux-Umgebung, sodass Sie die Kernels dort erst installieren und konfigurieren müssen.

Die nachfolgenden Code-Beispiele entstammen der Datei `.github/workflows/deploy-book-python-sparql-r.yml` welche die Installation und Konfiguration der drei Kernels vornimmt. Sie kann als Grundlage für spezielle Konfigurationen in Ihrem Book dienen.

### Python Kernel

Die Python-Einrichtung ist relativ unkompliziert, da der entspechende Kernel bei der Installation der benötigten Python-Pakete via `requirements.txt` installiert und konfiguriert wird:

```{literalinclude} ../.github/workflows/deploy-book-python-sparql-r.yml
:language: yaml
:lineno-match:
:start-after: "# Python"
:end-before: "# R"
```

### R Kernel

R erfordert etwas mehr Schritte, da wir nicht nur R und den passenden Kernel installieren, sondern diesen zudem für die Nutzung in Jupyter Notebooks registrieren müssen.

```{literalinclude} ../.github/workflows/deploy-book-python-sparql-r.yml
:language: yaml
:lineno-match:
:start-after: "# R"
:end-before: "# SPARQL"
```

Zusätzlich zum `IRkernel` wird auch das sog. `tidyverse` installiert, welches für die Arbeit mit Daten in R weit verbreitet ist.

### SPARQL Kernel einrichten

Die SPARQL Kernel-Installation ist einfach, sobald Python eingerichtet ist:

```{literalinclude} ../.github/workflows/deploy-book-python-sparql-r.yml
:language: yaml
:lineno-match:
:start-after: "# SPARQL"
:end-before: "# check all kernels"
```

### Mehrere Kernels kombinieren

Möchten Sie in einem Workflow mehrere Programmiersprachen unterstützen, so fügen Sie alle Einrichtungsschritte nacheinander ein. Entscheidend ist, dass sämtliche Kernel installiert sind, bevor der Build des Books gestartet wird. Nutzen Sie hierzu die Beispiele im vorliegenden Template.

### Kernels überprüfen

Es ist immer eine gute Praxis zu überprüfen, ob alle Ihre Kernels ordnungsgemäß installiert sind:

```{literalinclude} ../.github/workflows/deploy-book-python-sparql-r.yml
:language: yaml
:lineno-match:
:start-after: "# check all kernels"
:end-before: "# only caches"
```

Dieser Befehl zeigt Ihnen alle Kernels an, die GitHub Actions zur Ausführung Ihrer Notebooks verwenden kann.

Das Verständnis von Kernels hilft Ihnen bei der Fehlerbehebung, wenn Notebooks nicht ordnungsgemäß ausgeführt werden, und stellt sicher, dass Ihr Jupyter Book sowohl lokal als auch in automatisierten Umgebungen erfolgreich erstellt wird.


```{admonition} Zusätzliche Materialien
:class: seealso

Für detailliertere Informationen über Jupyter Kernels schauen Sie sich diese Ressourcen an:
- <a href="https://docs.jupyter.org/en/stable/projects/kernels.html" class="external-link" target="_blank">Offizielle Jupyter Kernels Dokumentation</a> 
- <a href="https://docs.jupyter.org/en/latest/install/kernels.html" class="external-link" target="_blank">Installation von Kernels</a> 
- <a href="https://jupyter-client.readthedocs.io/en/latest/kernels.html" class="external-link" target="_blank">Entwicklung eigener Kernels für Jupyter</a> 
- <a href="https://github.com/jupyter/jupyter/wiki/Jupyter-kernels" class="external-link" target="_blank">Liste verfügbarer Jupyter Kernels</a>

```