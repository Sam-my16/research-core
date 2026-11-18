# Plan de requisitos, implementación y prueba

Convertir una discusión en un documento que otro agente pueda ejecutar de punta
a punta sin volver a preguntar.

## Cuándo

Después de `discuss.md`, antes de tocar código, cuando el trabajo es más largo
que un par de pasos.

## Estructura

```markdown
# Plan — <título>

## Objetivo
Qué se quiere lograr, en una o dos frases.

## Criterios de éxito
Cómo se sabrá que está hecho. Verificables, no aspiracionales.
"El test X pasa", no "el modelo anda mejor".

## Contexto
Archivos relevantes con su ruta y estado (ACTIVE/FROZEN).
Qué NO se puede tocar.

## Etapas
Por etapa:
- objetivo
- archivos que se van a tocar
- cómo se verifica que la etapa está bien
- parada explícita del usuario, si la hay

## Riesgos
Qué puede salir mal y qué se hace si sale mal.

## Fuera de alcance
Lo que explícitamente NO se hace en este plan.
```

## Reglas

**Criterios verificables.** Si el criterio no se puede comprobar corriendo algo
o mirando una figura, no es un criterio, es un deseo.

**Etapas verificables.** Durante la ejecución, comprobá el resultado de cada
etapa. Si cumple el criterio y la siguiente etapa forma parte del pedido,
continuá. Respetá las paradas explícitas del usuario.

**Los artefactos FROZEN se listan explícitamente** como intocables. Se pueden
leer, copiar y llamar; no modificar.

**Fuera de alcance es obligatorio.** La sección que evita que el trabajo se
expanda sola. Si está vacía, el plan no está pensado.

## Verificación antes de ejecutar

Antes de empezar a implementar, releer el plan y confirmar:

- ¿un agente sin este contexto podría ejecutarlo?
- ¿los criterios de éxito son comprobables?
- ¿está claro qué no se puede tocar?

Si alguna respuesta es no, el plan todavía no está listo.
