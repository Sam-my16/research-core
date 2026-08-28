# Registrar un experimento

Una entrada por experimento, escrita **antes** de mirar el resultado.

## Parámetros

- `{destino}` — `explorations/<id>/log.md` o `runs/<id>/log.md`

## Por qué escribir la predicción antes

Si anotás qué esperabas después de ver el resultado, vas a anotar que lo
esperabas. Ese sesgo borra exactamente la información que sirve: la distancia
entre lo que creías y lo que pasó.

## Formato

```markdown
## <fecha> — <título corto>

**Hipótesis:** qué creo que va a pasar y por qué.
**Predicción:** el número o comportamiento concreto que espero.

**Cambio:** qué modifiqué respecto del experimento anterior. Uno solo.

**Configuración:**
- commit: `a3f21b9`
- semilla: 42
- comando: `python train.py --config configs/cae_base.yaml`
- datos: DTD, split train, 4512 muestras

**Resultado:** el número, sin adjetivos.

**Sorpresa:** en qué se diferenció de la predicción.

**Decisión:** qué hago a partir de esto.
```

## El campo Sorpresa

Es el más importante y el que más se omite. Escribí "ninguna" sólo después de
pensarlo en serio.

Qué capturar:

- ¿El resultado coincidió con la predicción? ¿Por cuánto no?
- ¿Se rompió algo que no debería haberse roto?
- ¿Algo funcionó por una razón distinta de la que suponías?
- ¿Algo tardó mucho más o mucho menos de lo previsto?

Las sorpresas acumuladas son el registro de dónde tu modelo mental del problema
estaba equivocado. Releerlas antes de escribir la discusión de la tesis vale
más que releer los resultados: los resultados ya están en las tablas, las
sorpresas no están en ningún otro lado.

## Un cambio por vez

Si modificás la arquitectura y la pérdida en el mismo experimento, el resultado
no te dice cuál de las dos hizo la diferencia. Cuando haya apuro y cambies
varias cosas juntas, anotalo explícitamente: **experimento no atribuible**.

## Resultados negativos

Se registran igual. Un experimento que falló y quedó documentado evita repetirlo
en tres meses. Uno que falló y no se anotó se repite siempre.

## Relación con otros workflows

- Antes de reportar el número: `sanity-check.md`
- Antes de que el número entre en `docs/`: `provenance.md`
