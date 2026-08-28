# Trazabilidad: de dónde salió cada figura y cada número

Que toda figura y todo número de la tesis se pueda rastrear hasta el script,
los datos, el commit y la semilla que lo produjeron.

## Parámetros

- `{artefacto}` — figura, tabla o número a rastrear, o un directorio a auditar

## Por qué

La pregunta "¿de dónde salió esta figura?" llega siempre: en una reunión con tu
director, en la defensa, o seis meses después cuando querés rehacerla con otro
dataset. Sin trazabilidad la respuesta es una tarde de arqueología sobre
notebooks, y a veces la respuesta honesta es "no sé".

## Regla

Toda figura o número que sale de `explorations/` hacia `docs/`, la tesis o una
presentación lleva un registro de procedencia.

## El registro

Un archivo `PROVENANCE.md` en `docs/`, con una entrada por artefacto:

```markdown
### figura 4.2 — curvas de reconstrucción CAE vs. CVAE sobre DTD

- **Archivo:** `docs/figuras/fig_4_2_cae_cvae.png`
- **Producido por:** `runs/2026-08-20_cae-dtd-baseline/plot_curves.py`
- **Datos de entrada:** DTD vía `torchvision.datasets.DTD`, split `train`
- **Commit:** `a3f21b9`
- **Semilla:** 42
- **Comando:** `python plot_curves.py --run runs/2026-08-20_cae-dtd-baseline`
- **Estado:** FROZEN
- **Controles:** `runs/2026-08-20_cae-dtd-baseline/sanity.md` — todos pasan
```

Los campos que no aplican se omiten. Los que aplican y no se saben se escriben
como **desconocido**, no se dejan en blanco: un campo vacío parece un olvido de
formato, "desconocido" es información real.

## Procedimiento

### Al promover un resultado

1. Identificar el script exacto que lo produjo. Si fue un notebook, anotar el
   notebook **y la celda**; si el notebook cambió desde entonces, decirlo.
2. Registrar el commit con `git rev-parse --short HEAD`. Si el árbol estaba
   sucio al correrlo, anotarlo: un commit no describe código sin commitear.
3. Anotar la semilla. Si no se fijó ninguna, escribir **sin semilla fijada** —
   eso dice que el número no es exactamente reproducible, y es un dato válido.
4. Enlazar los controles de `sanity-check`. Un número sin controles no debería
   estar en `docs/`.

### Al auditar

Recorrer las figuras de `docs/` y para cada una comprobar que:

- el script referenciado sigue existiendo
- el commit sigue existiendo en la historia
- los datos de entrada siguen accesibles

Reportar las que no se pueden rastrear. **No inventes la procedencia de una
figura vieja**: si no se sabe, se marca como no rastreable y se decide si vale
la pena regenerarla.

## Regenerar como prueba

La prueba real de trazabilidad no es el registro: es poder ejecutar el comando
anotado y obtener la misma figura.

Antes de entregar la tesis, elegí dos o tres figuras centrales y regeneralas
desde cero siguiendo sólo lo que dice `PROVENANCE.md`. Lo que falle ahí es
exactamente lo que va a fallar cuando alguien pregunte.

## Interacción con FROZEN

Una vez que una figura entra en la tesis, la corrida que la produjo se congela
(ver `rules/LAYOUT.md`). El registro de procedencia y el archivo `FROZEN` son
las dos mitades de lo mismo: uno dice de dónde vino, el otro impide que cambie
por debajo.
