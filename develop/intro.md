---
lang: de-DE
---
# Einführung in die Entwicklungsumgebung

Für jede QUADRIGA OER, die als Jupyter Book entwickelt wird, sollte die automatische Erstellung der Website per Github Actions aktiviert sein. Dadurch werden Änderungen im Haupt-Entwicklungsstrang (`main`-branch in Git) automatisch gebaut, wenn sie in Github veröffentlicht werden. Kleinere Änderungen wie bspw. die Behebung von Tippfehlern können daher sogar über die Web-Oberfläche von Github getätigt werden. Größere Änderungen und die experiementelle (und ggf. private) Weiterentwicklung benötigen jedoch eine lokale Entwicklungsumgebung. Empfehlungen dazu, wie Sie diese bei sich einrichten können, werden in den nachfolgenden Abschnitten beschrieben.

## Bestandteile der Entwicklungsumgebung
Die Entwicklungsumgebung besteht aus verschiedenen Software-Komponenten. Diese sind Git, eine Python-Distribution sowie Jupyter Book und andere Python-Programmbibliotheken, die in der OER genutzt werden sollen. Werden andere Programmiersprachen wie bspw. R genutzt, so müssen diese und alle nötigen Programmbibliotheken zusätzlich in der Lokalen Umgebung (und in der Github Action) vorhanden sein.

Konkret benötigen Sie:
- Git, um die Versionsverwaltung durchzuführen und um mit Github zu interagieren;
- Python – vorzugsweise über die Anaconda Distribution –, um Jupyter Book lokal nutzen zu können und ggf. für Inhalte der OERs;
- Jupyter Book, um während des Schreibens lokal die Markdown-Dateien und Jupyter Notebooks in eine Website-Ansicht zu transformieren;
- sowie ggf. ein Editor oder eine IDE wie VSCode, wenn die Bearbeitung der Dateien nicht über die Jupyter Notebook- oder Jupyter Lab-Oberfläche aus der Anaconda Distribution erfolgen soll;
- und ggf. eine grafische Oberfläche für Git wie Github Desktop.

## Aufbau dieses Buchteils
Dieser Buchteil stellt Ihnen nach der Einleitung kurz die einzelnen Software-Komponenten vor und gibt dann jeweils Hinweise zur Installation und der Nutzung der jeweiligen Software. Im Anschluss wird der ganzheitliche Ablauf und das Zusammenspiel der einzelnen Software für die Entwicklung der QUADRIGA OERs beispielhaft dargestellt.

