---
lang: de-DE
---

(formatierung:Carousel)=
# Carousel

Mit Sphinx können Sie interaktive Carousels erstellen, um Inhalte ansprechend und strukturiert zu präsentieren. Ein Carousel ist eine Sammlung von Elementen, die horizontal durchgeblättert werden können. Dies ist besonders nützlich, um mehrere Elemente platzsparend darzustellen.


Verwenden Sie die folgende Syntax, um ein Carousel zu erstellen:
`````
````{card-carousel} 1

```{card}
:class-card: carousel-card

![Folie1](Bildpfad)
```

```{card}
:class-card: carousel-card

![Folie2](Bildpfad)
```
````

```{card}
:class-card: carousel-card

![Folie3](Bildpfad)
```
````
`````


````{card-carousel} 1

```{card}
:class-card: carousel-card
![image1](../assets/slides/1.jpg)
```

```{card}
:class-card: carousel-card
![image2](../assets/slides/2.jpg)
```

```{card}
:class-card: carousel-card
![image3](../assets/slides/3.jpg)
```

````

