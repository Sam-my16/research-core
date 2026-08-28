# Organización del proyecto y estados de artefacto

Define **dónde vive cada cosa** y **qué se puede creer**. Cómo se comporta el
agente está en `CONTRACT.md`.

## Estructura mínima

Sólo `docs/` es obligatorio. El resto se crea cuando hace falta.

```
<proyecto>/
├── docs/            # documentación confiable: decisiones, resultados, índice
├── src/             # código promovido, reusable, mantenido
├── explorations/    # trabajo activo y descartable: pruebas, spikes
└── runs/            # ejecuciones reproducibles: configs, logs, salidas
```

No hace falta inventar directorios para que el proyecto "parezca" ordenado. Un
directorio vacío es ruido; borralo.

## Escalera de confianza

Que un archivo exista no lo hace confiable. En orden:

1. **`docs/RESULTS.md`** y **`src/`** — resultados validados y código promovido.
   Se pueden citar como ciertos.
2. **Handoffs** (`HANDOFF_*.md`) — qué se hizo, con qué evidencia.
3. **`explorations/`** — descartable. Puede estar mal, incompleto o
   contradecirse consigo mismo. **No es evidencia de nada.**
4. **Notas sueltas y chat** — no autoritativo.

Antes de tratar un resultado como cierto, mirá en ese orden. Si un número está
sólo en un notebook de `explorations/`, todavía no es un resultado: es una
observación.

### Promoción

Mover algo de `explorations/` a `src/` o a `docs/RESULTS.md` requiere:

- anotar los supuestos y decisiones en `docs/`
- que el código promovido tenga alguna prueba mínima
- marcar o borrar lo exploratorio que quedó obsoleto

La promoción es un acto explícito. Nada asciende solo por antigüedad.

## Estados: ACTIVE y FROZEN

Aplica a exploraciones, corridas y artefactos derivados.

**ACTIVE** — se puede modificar, retomar y corregir. Es el estado por defecto.

**FROZEN** — referencia sellada e inmutable. No se modifica, no se vuelve a
correr, no se reinterpreta a posteriori. Se puede leer, copiar y citar.

Un directorio se congela creando un archivo `FROZEN` adentro, con la fecha y el
motivo:

```
runs/2026-08-20_cae-dtd-baseline/FROZEN
```

### Por qué existe FROZEN

Cuando un número entra en la tesis, el artefacto que lo produjo deja de ser
código de trabajo y pasa a ser evidencia. Si después se modifica —aunque sea
para "mejorarlo"— el número del capítulo deja de tener respaldo y nadie se
entera.

Congelar no es burocracia: es lo que permite escribir "figura 4.2, generada por
`runs/2026-08-20_cae-dtd-baseline/`" y que siga siendo verdad en noviembre.

### Qué hacer en vez de descongelar

Si una corrida congelada tiene un error, **no la corrijas**. Creá una nueva,
anotá en `docs/` qué estaba mal en la anterior, y actualizá lo que dependía de
ella. La corrida vieja queda como registro de lo que efectivamente se hizo.

### Cumplimiento

`scripts/check_frozen.py` bloquea los commits que tocan archivos bajo un
directorio congelado. Se instala apuntando `core.hooksPath` a un directorio
versionado — `.git/hooks/` no viaja con el clon.

La regla escrita es orientación; el hook es lo que efectivamente la sostiene.

## Datos

Los datos crudos no se versionan. Se versiona **cómo obtenerlos**: la URL, el
script de descarga, el hash si importa.

Si un dato no se puede volver a conseguir, dejá constancia explícita en
`docs/` de dónde está la única copia.
