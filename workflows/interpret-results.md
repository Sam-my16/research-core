# Interpretar resultados (figuras primero)

Producir un documento que explique qué muestran los resultados, apoyado en
figuras antes que en métricas escalares.

## Parámetros

- `{artefacto}` — directorio de la corrida o exploración a interpretar

## Por qué figuras primero

Un escalar comprime demasiado. Un `val_loss` que baja es compatible con un
modelo que aprendió, con uno que predice siempre la clase mayoritaria, y con
uno que memorizó el conjunto de validación por fuga. La figura distingue los
tres casos; el número no.

Para datos con estructura espacial esto es todavía más marcado: una exactitud
global alta puede convivir con un mapa de clasificación que es visiblemente
ruido en las zonas que importan.

## Procedimiento

### 1. Mirar antes de escribir

Abrí las figuras. Si no hay figuras, generalas antes de interpretar nada.

Mínimo para un experimento de entrenamiento:

- curvas de pérdida de train y validación en el mismo eje
- distribución de las predicciones (no sólo la métrica agregada)
- ejemplos concretos: los mejores, los peores, y algunos al azar
- para clasificación: matriz de confusión
- para reconstrucción: entrada, salida y residuo lado a lado

El residuo es el que más información tiene y el que menos se mira. Si el
residuo tiene estructura, el modelo no capturó algo sistemático.

### 2. Una afirmación por figura

Para cada figura, tres líneas:

```markdown
### fig_03_residuos.png

**Afirmación:** el residuo conserva estructura espacial en las zonas urbanas.
**Evidencia visual:** franjas verticales visibles en el cuadrante superior
derecho, ausentes en las zonas de agua.
**Implicación:** la pérdida MSE no está penalizando el error de fase; coincide
con lo que predice Lee 1994 sobre usar estadística de Wishart.
```

Si no podés escribir la evidencia visual sin recurrir a lo que ya creías, la
figura no muestra lo que pensás que muestra.

### 3. Anomalías y sorpresas

Sección aparte para lo que no encaja. Todo lo que sea raro va acá aunque no
tengas explicación: una curva con un salto, una clase que anda mucho mejor de
lo esperable, un tiempo de cómputo desproporcionado.

**Lo raro que no se anota se olvida, y suele ser lo importante.** Una métrica
sospechosamente buena es un hallazgo, no un logro: mandá a correr
`sanity-check.md` antes de celebrarla.

### 4. Volver a los objetivos

Cerrar contrastando con lo que se buscaba. Tres respuestas posibles y las tres
son válidas:

- se cumplió, con esta evidencia
- no se cumplió, y esto es lo que se aprendió
- no se puede saber todavía, falta esto

La tercera es una respuesta legítima. Forzar una conclusión donde la evidencia
no alcanza es peor que decir que no alcanza.

## Salida

`docs/RESULTS_REVIEW_<fecha>.md`, o dentro del directorio de la corrida.

Las figuras se referencian por ruta relativa, nunca se describen de memoria.

## Límite

Este workflow interpreta, no valida. Un número no entra en `docs/RESULTS.md`
sin haber pasado `sanity-check.md` primero.
