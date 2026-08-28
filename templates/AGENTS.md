# AGENTS.md — {PROJECT_NAME}

Instrucciones para cualquier agente de IA que trabaje en este repositorio.

Este archivo sigue el formato [AGENTS.md](https://agents.md/), que leen Cursor,
Codex, Gemini CLI, Copilot, Aider, Zed, Windsurf y otros. Claude Code lee
`CLAUDE.md`, que en este repo es una línea que importa este archivo.

El contenido vive en `.agent/`, copiado desde
[research-core](../research-core). Versión instalada: ver `.agent/VERSION`.

<!-- research-core:inicio — este bloque lo regenera install.py, no lo edites a mano -->

## Reglas

Se aplican siempre. Leelas antes de trabajar.

- **`.agent/rules/CONTRACT.md`** — cómo comportarse: modos, cuándo parar,
  evidencia antes que explicación, nada implícito.
- **`.agent/rules/LAYOUT.md`** — dónde vive cada cosa, escalera de confianza,
  estados ACTIVE/FROZEN.
- **`.agent/rules/NOTEBOOKS.md`** — texto plano como fuente de verdad.

### Lo mínimo que hay que saber

**Nada es confiable por defecto.** Un número que está sólo en un notebook de
`explorations/` es una observación, no un resultado. Para creerle tiene que
estar en `docs/RESULTS.md` o en `src/`.

**FROZEN es inmutable.** Un directorio con un archivo `FROZEN` adentro no se
modifica ni se vuelve a correr. Se puede leer y copiar. Hay un hook de git que
lo bloquea.

**No adivines la fecha.** Ejecutá `date +%Y-%m-%d_%H%M%S`.

**No hagas commit salvo que te lo pidan.**

## Workflows

Instrucciones para tareas concretas. Se invocan diciendo *"seguí
`.agent/workflows/<nombre>.md`"*, o por su nombre si tu herramienta los expone
como comandos.

| Workflow | Para qué |
|---|---|
| `discuss` | Analizar y proponer caminos, **sin tocar nada** |
| `plan` | Convertir una discusión en un plan ejecutable |
| `experiment-log` | Registrar un experimento, con el campo Sorpresa |
| `sanity-check` | Controles antes de creerse un resultado de ML |
| `interpret-results` | Interpretar resultados, figuras primero |
| `provenance` | Rastrear una figura hasta script, datos, commit y semilla |
| `handoff` | Entregar el turno a otra sesión o agente |
| `paper-slides` | Diapositivas de un paper, todo citado y verificable |
| `paper-note` | Nota de lectura estructurada de un paper |

## Verificaciones

```bash
python .agent/scripts/verify_citations.py <deck>/slides.md   # citas de un deck
python .agent/scripts/ingest_paper.py --check <dir>          # conversiones rotas
python .agent/scripts/check_frozen.py --list                 # qué está congelado
```

<!-- research-core:fin -->

## Específico de este proyecto

Todo lo que va debajo de esta línea es propio del repositorio y `install.py` no
lo toca.
