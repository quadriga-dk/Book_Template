---
lang: de-DE
---

(formatierung:neuer_tab)=
# Link in neuem Tab öffnen

Ein in Markdown gesetzter Link öffnet normalerweise im gleichen Browsertab. Das ist für die Nutzung in einer OER nicht ideal. Daher sollten diese Links wie folgt als HTML-Link gesetzt werden:
```html
<a href="https://example.com" target="_blank">Linktext</a>
```
<a href="https://example.com" target="_blank">Linktext</a>

Verweist der Link auf eine externe Seite, so muss dies zudem durch Zuweisung der CSS-Klasse `.external-link` gekennzeichnet werden:
```html
<a href="https://example.com" class="external-link" target="_blank">Linktext</a>
```
<a href="https://example.com" class="external-link" target="_blank">Linktext</a>