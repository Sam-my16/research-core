# Controles antes de creerse un resultado

Se corre **antes** de reportar una métrica, escribirla en `docs/RESULTS.md` o
ponerla en la tesis. No después.

## Parámetros

- `{artefacto}` — el notebook, script o corrida que produjo el resultado

## Por qué

Un resultado bueno no es evidencia de que el modelo funcione: es evidencia de
que *algo* produjo ese número. Casi siempre que un modelo da mucho mejor de lo
esperado, la causa es una fuga de información, no una arquitectura brillante.

Estos controles cuestan minutos. Descubrir la fuga después de escribir el
capítulo cuesta el capítulo.

## Los controles

### 1. Baseline trivial

Comparar contra el predictor más tonto posible:

- clasificación: predecir siempre la clase mayoritaria
- reconstrucción: predecir la media del dataset, o devolver la entrada sin tocar
- regresión: predecir la media

**Si el modelo no le gana claramente al baseline trivial, no hay resultado.**
Un autoencoder que "reconstruye bien" puede estar aprendiendo la identidad.

### 2. Etiquetas barajadas

Entrenar el mismo modelo con las etiquetas permutadas al azar.

Debería colapsar a la performance del azar. **Si sigue aprendiendo algo, hay
fuga**: la señal está entrando por un camino que no es el que creés.

Para autoencoders, el equivalente es entrenar con pares (entrada, objetivo)
desapareados: la pérdida debería quedarse en el nivel de reconstruir la media.

### 3. Sobreajustar un solo batch

Entrenar sobre 8–32 muestras hasta que la pérdida se vaya casi a cero.

Si **no** lo logra, hay un bug: gradientes que no fluyen, learning rate
inservible, pérdida mal conectada, target mal alineado. Este control detecta en
dos minutos bugs que de otro modo se disfrazan de "el modelo no converge".

### 4. Fuga entre train y test

El control más importante y el más fácil de arruinar.

Preguntas obligatorias:

- ¿Alguna muestra de test aparece, aunque sea parcialmente, en train?
- ¿La normalización se calculó **sobre todo el dataset** antes de partirlo?
  (media y desvío del conjunto completo son fuga)
- ¿El aumento de datos se aplicó antes de la partición?
- ¿La selección de hiperparámetros usó el test set?

**Para datos con estructura espacial (imágenes SAR, series temporales), partir
al azar por píxel o por ventana es fuga garantizada.** Parches vecinos de la
misma escena comparten speckle, iluminación y clase: un parche en test cuyo
vecino está en train ya fue visto en la práctica. La partición tiene que ser
por región disjunta, por escena o por bloque temporal.

Este es el error que produce 98% de exactitud y un modelo que no generaliza a
nada.

### 5. Balance de clases

Reportar la distribución de clases junto a la métrica. Con clases desbalanceadas,
la exactitud global es engañosa: informar matriz de confusión, o exactitud por
clase, o kappa.

### 6. Determinismo

Correr dos veces con la misma semilla y confirmar que da lo mismo. Si no, hay
aleatoriedad sin fijar y los números no son comparables entre experimentos.

Después correr con **tres semillas distintas** y reportar la dispersión. Una
mejora de 0.4 puntos entre dos modelos no significa nada si la varianza entre
semillas es de 2 puntos.

### 7. Que las unidades y los rangos cierren

- ¿Las entradas están en el rango que la arquitectura espera?
- Para datos complejos: ¿la fase se preservó, o se perdió en algún casteo a real?
- ¿La pérdida es la que corresponde a la estadística del dato, o se usó MSE
  por costumbre sobre datos que no son gaussianos?

## Salida

Una sección en el log del experimento, o un archivo `sanity.md` junto al
artefacto:

```markdown
## Controles — <fecha> — <artefacto>

| Control | Resultado |
|---|---|
| Baseline trivial | modelo 0.82 vs. mayoritaria 0.61 — pasa |
| Etiquetas barajadas | 0.24 (azar = 0.25) — pasa |
| Sobreajuste de un batch | pérdida 3.1 -> 0.004 en 200 pasos — pasa |
| Fuga train/test | partición por región disjunta, verificada — pasa |
| Balance de clases | 61/22/11/6 %, se reporta por clase |
| Determinismo | 3 semillas: 0.82 / 0.80 / 0.83 (sd 0.015) |

**No verificado:** <lo que quedó pendiente y por qué>
```

Los controles que no corriste se listan como no verificados. No se omiten.

## Cuando un control falla

Falla un control, **el resultado no se reporta**. No se reporta con una nota al
pie, no se reporta "provisoriamente". Se arregla la causa y se vuelve a correr.

Si no se puede arreglar ahora, el resultado queda en `explorations/` y no sube
a `docs/RESULTS.md`.
