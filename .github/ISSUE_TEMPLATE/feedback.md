---
name: Feedback
description: Nutzen Sie diese Vorlage, um Feedback zur Fallstudie zu geben
labels: ["feedback"]
body:
 - type: markdown
   attributes:
     value: |
       Vielen Dank für Ihr Feedback! Ihre Rückmeldung hilft uns, die Materialien gezielt zu verbessern.

 - type: input
   id: section
   attributes:
     label: Abschnitt/Modul
     description: Auf welchen Teil der Fallstudie bezieht sich Ihr Feedback?
     placeholder: "z.B. Kapitel B, Abschnitt 2, gesamtes Jupyter Book"
   validations:
     required: false

 - type: dropdown
   id: feedback-type
   attributes:
     label: Art des Feedbacks
     options:
  - Inhalt & Aufbau
  - Methodik & Didaktik
  - Beispiele & Übungen
  - Technische Aspekte
  - Praxisrelevanz
  - Textliche Überarbeitung
  - Sonstiges
   validations:
     required: true

 - type: textarea
   id: feedback
   attributes:
     label: Ihr Feedback
     description: Was möchten Sie uns mitteilen?
     placeholder: Bitte beschreiben Sie Ihr Feedback so konkret wie möglich.
   validations:
     required: true

 - type: textarea
   id: suggestion
   attributes:
     label: Verbesserungsvorschlag
     description: Haben Sie einen konkreten Vorschlag zur Verbesserung?
     placeholder: Optional - Ihre Ideen für mögliche Verbesserungen
   validations:
     required: false
---