# Entregar el turno

Escribir un documento que le permita a alguien sin memoria de esta conversación
retomar el trabajo exactamente donde quedó.

## Cuándo

- la sesión termina o el contexto se satura
- se completó una unidad de trabajo con sentido
- se congela una fase
- sigue otro agente, u otra herramienta

## Nombre del archivo

Ejecutá el comando, no adivines la fecha:

```bash
date +%Y-%m-%d_%H%M%S
```

Resultado: `HANDOFF_2026-08-28_164500.md`

La fecha en el nombre es sólo para leerlo cómodo. **Para ordenar
cronológicamente usá la fecha de modificación del archivo**, no la del nombre:
un handoff puede escribirse con la fecha mal.

## Estructura

```markdown
# Handoff — <fecha>

## Contexto de entrada
Archivos y artefactos con los que se trabajó, con su estado (ACTIVE/FROZEN).

## Qué se hizo
Comandos ejecutados y operaciones sobre archivos. Exactos, copiables.

## Evidencia
Salidas verbatim de pruebas y verificaciones. Rutas a figuras y logs.
No "los tests pasan": la salida.

## Contexto de salida
Archivos creados o modificados, con rutas. Estado de cada uno.

## Qué falta
Lo que quedó sin hacer, y lo que se intentó y no funcionó.
Los caminos ya descartados valen tanto como los pendientes.

## Próxima tarea
Una sola, concreta.
```

## Reglas

**Sin memoria implícita.** Todo lo que hace falta para continuar está en el
documento o en un archivo que el documento nombra. Si algo importante se
decidió sólo en el chat, va acá.

**Los handoffs no se editan.** Una vez escrito queda como registro de lo que se
sabía en ese momento. Si algo estaba mal, se corrige en el siguiente y se
aclara qué cambió.

**Rutas, no descripciones.** "El notebook del autoencoder" no sirve;
`codigos/CAE_CVAE_DTD.ipynb` sí.

**Lo que no funcionó es contenido de primera.** Sin eso el próximo repite los
mismos tres intentos fallidos.

## Retomar

Al arrancar una sesión nueva:

1. Buscar el handoff más reciente **por fecha de modificación**
2. Leerlo entero antes de tocar nada
3. Verificar que el estado descrito coincide con el disco — los archivos pueden
   haber cambiado desde entonces
4. Confirmar qué está FROZEN antes de escribir

Si el handoff y el disco no coinciden, decilo antes de seguir. No asumas cuál
de los dos tiene razón.
