# Videos einbetten
Da in Markdown auch HTML-Tags genutzt werden können, können diese für die Einbettung von Videos genutzt werden. Liegt die Datei vor, so kann das `video`-Tag genutzt werden. Häufiger jedoch findet die Einbettung per `iframe` statt.

## YouTube
Das nachfolgende Beispiel zeigt die Einbettung eines Videos aus YouTube. Andere Video-Hosting-Systeme nutzen leicht abgewandelte Versionen dieser Einbettung. Sehen Sie sich dazu die Dokumentation Ihrer Video-Platform an. Das Beispiel unten ist direkt aus YouTube kopiert – über *Teilen* und dann *Einbetten* – bis auf die Entfernung des Tracking-Parameters (`?si=………`) in der `src`-URL.
```html
<iframe width="560" height="315" src="https://www.youtube.com/embed/MDMUiQ2_ZWE"
title="YouTube video player" frameborder="0"
allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
</iframe>
```
<iframe width="560" height="315" src="https://www.youtube.com/embed/MDMUiQ2_ZWE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## VideoUP (Panopto)

```html
<iframe src="https://videoup.uni-potsdam.de/Panopto/Pages/Embed.aspx?id=8e87d499-79fb-4e65-905b-b1d30087d1e9&autoplay=false&offerviewer=false&showtitle=false&showbrand=false&captions=true&interactivity=all"
height="405" width="720" style="border: 1px solid #464646;" allowfullscreen allow="autoplay">
</iframe>
```
<iframe src="https://videoup.uni-potsdam.de/Panopto/Pages/Embed.aspx?id=8e87d499-79fb-4e65-905b-b1d30087d1e9&autoplay=false&offerviewer=false&showtitle=false&showbrand=false&captions=true&interactivity=all" height="405" width="720" style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>