---
name: Frage
description: Nutzen Sie diese Vorlage, um eine Frage zu dieser Fallstudie zu stellen
labels: ["question"]
body:
  - type: markdown
    attributes:
      value: |
        Vielen Dank, dass Sie sich die Zeit nehmen, eine Frage zu stellen!

  - type: input
    id: section
    attributes:
      label: Abschnitt/Modul
      description: Zu welchem Teil der Fallstudie ist Ihre Frage?
      placeholder: "z.B. Kapitel B, Abschnitt 2"
    validations:
      required: false

  - type: textarea
    id: question
    attributes:
      label: Ihre Frage
      description: Was möchten Sie wissen?
      placeholder: Bitte formulieren Sie Ihre Frage so präzise wie möglich.
    validations:
      required: true

  - type: dropdown
    id: question-type
    attributes:
      label: Art der Frage
      options:
        - Verständnis des Inhalts
        - Technische Umsetzung
        - Forschungsdesign & Methodik
        - Datenbezogen
        - Sonstiges
    validations:
      required: true
---