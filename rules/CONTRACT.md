# Contrato del agente

Cómo se comporta un agente trabajando en este proyecto. Dónde vive cada cosa
está en `LAYOUT.md`.

## Qué se busca

Que el trabajo asistido por IA sea **reproducible** (otro puede re-correrlo),
**auditable** (la evidencia existe en archivos, no en el chat) y **seguro**
(nada se pisa por accidente).

## Invariantes

### Nada implícito

No asumas unidades, convenciones, significado de un dataset, semillas ni
intención. Si algo es ambiguo y afecta la corrección del resultado: **pará y
preguntá**. Una suposición silenciosa que resulta falsa cuesta más que una
pregunta.

### Evidencia antes que explicación

Preferí inspeccionar el código, correr una prueba o generar una figura antes
que razonar en prosa sobre lo que probablemente pasa. Cuando especules,
marcalo como especulación.

Un argumento largo sobre por qué el modelo debería funcionar vale menos que
un gráfico de la curva de pérdida.

### El chat no es un artefacto

Si algo importa, va a un archivo. Las conclusiones que viven sólo en la
conversación se pierden en la próxima sesión y no se pueden citar.

### Reproducibilidad cuando se afirma

Si decís que algo es reproducible, dejá los inputs fijados y el comando exacto.
Si hay aleatoriedad, la semilla y la configuración van escritas.

## Alcance del pedido

**Revisión.** Si el usuario pide analizar, comparar o recomendar, inspeccioná
la evidencia y respondé en la conversación sin crear ni modificar archivos.
Si queda una duda, proponé la comprobación mínima que la resolvería.

**Ejecución.** Si pide crear, corregir o verificar un entregable, seguí hasta
comprobar el resultado dentro del alcance pedido. Respetá las paradas
explícitas. Cuando ejecutes una prueba o corrida, registrá el intérprete,
el entorno y el comando.

«Revisá y corregí» incluye aplicar y verificar la corrección. «Revisá y
decime qué corregirías» termina con la recomendación.

## Entregar el turno

La sesión termina, el contexto se satura, o sigue otro agente.

Producí un handoff que le alcance a alguien sin memoria de esta conversación.
Ver `workflows/handoff.md`.

## Trabajo científico

- **Código antes que conjetura.** Si el código existe, leelo antes de suponer
  qué hace.
- **Figuras antes que métricas escalares** para diagnosticar. Un `val_loss` que
  baja puede esconder un modelo que predice siempre la clase mayoritaria.
- **Un resultado que no sorprende a nadie merece desconfianza.** Si el número
  salió exactamente como esperabas a la primera, buscá el error antes de
  festejar.

## Fechas

Nunca adivines la fecha. Ejecutá:

```bash
date +%Y-%m-%d_%H%M%S
```

Los agentes se equivocan de fecha sistemáticamente y un timestamp inventado
corrompe el orden cronológico de los handoffs. Para ordenar por antigüedad usá
la fecha de modificación del archivo, no la del nombre.

## Límites

- No modifiques `src/` sin instrucción explícita en esta sesión.
- No toques nada bajo un directorio `FROZEN`.
- No hagas commit ni push salvo que te lo pidan.
