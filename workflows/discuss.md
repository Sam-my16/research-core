# Discutir y planificar

Analizar un pedido, reunir información del código y los artefactos, y proponer
caminos posibles. **No se ejecuta ninguna acción.**

## Parámetros

- `{pedido}` — la pregunta o el problema a discutir

## Regla

Modo B del contrato: leer, diagnosticar, recomendar, **parar**. No se crean ni
se modifican archivos. Ni siquiera "uno chiquito para probar".

## Procedimiento

1. **Leer primero.** Auditá el código y los artefactos relevantes antes de
   hipotetizar. Si el código existe, leelo; no supongas qué hace por su nombre.

2. **Reunir el estado real.** Qué hay, qué está ACTIVE, qué está FROZEN, qué
   dicen los handoffs recientes y `docs/RESULTS.md`.

3. **Separar lo que se sabe de lo que se supone.** Marcá explícitamente cuál es
   cuál. Una suposición presentada como hecho es el modo más común de arruinar
   una decisión.

4. **Proponer opciones, no una sola.** Dos o tres caminos con su costo, su
   riesgo y qué haría falta para decidir entre ellos. Con una recomendación
   propia y el motivo.

5. **Nombrar el diagnóstico que resolvería la duda.** Si la decisión depende de
   algo que no se sabe, decí qué prueba, figura o medición mínima lo
   resolvería. Eso vale más que seguir argumentando.

## Salida

Respuesta en la conversación. Si la discusión fue larga o la decisión importa,
ofrecé escribirla en `docs/` — pero escribirla es otra acción, y se pide
aparte.

## Parada

Recomendación con próximos pasos concretos, y **parar**. No empieces a
implementar porque la conclusión parezca obvia.
