# research-core

Reglas, workflows y verificadores para trabajo de investigación asistido por IA.

Pensado para uso individual en proyectos científicos: una tesis, un paper, una
serie de experimentos. Se instala dentro de cada proyecto y viaja con él.

## Principio de diseño

**El contenido es neutro; los adaptadores son descartables.**

Ningún archivo de `rules/` o `workflows/` menciona una herramienta de IA. La
entrada es `AGENTS.md`, el formato que leen Cursor, Codex, Gemini CLI, Copilot,
Aider, Zed y Windsurf. Claude Code lee `CLAUDE.md`, que acá es una sola línea
importando `AGENTS.md`.

Cambiar de herramienta significa escribir un adaptador de ~30 líneas, no
reescribir el contenido. Y en el peor caso, los workflows son markdown plano:
funcionan diciéndole a cualquier agente *"leé este archivo y seguilo"*, o
pegándolos a mano en un chat.

## Qué hay

```
rules/        reglas que aplican siempre
workflows/    instrucciones para tareas concretas
scripts/      verificadores (sin dependencias externas)
templates/    AGENTS.md y plantilla de deck Slidev
hooks/        hook de git que se instala vía core.hooksPath
adapters/     traducción a cada herramienta
install.py    instalador
```

## Instalar

```bash
python install.py /ruta/al/proyecto --tools claude
```

Copia el contenido a `<proyecto>/.agent/`, genera `AGENTS.md`, configura
`core.hooksPath` y aplica los adaptadores. Para actualizar más adelante:

```bash
python install.py /ruta/al/proyecto --update
```

Se copia en vez de usar submódulo o symlink: el proyecto queda autocontenido —
el día que entregues la tesis, las reglas viajan adentro— los symlinks en
Windows requieren Developer Mode, y los submódulos son fricción pura para
trabajo individual. `.agent/VERSION` registra desde qué commit se copió.

## Las tres ideas que lo sostienen

### 1. Nada es confiable por defecto

Un número que está sólo en un notebook de `explorations/` es una observación,
no un resultado. Para creerle tiene que estar promovido a `docs/RESULTS.md` o
a `src/`. Ver `rules/LAYOUT.md`.

### 2. Lo que es evidencia se congela

Cuando un número entra en la tesis, el artefacto que lo produjo deja de ser
código de trabajo. Un archivo `FROZEN` en el directorio lo vuelve inmutable, y
un hook de git bloquea los commits que lo toquen.

La regla escrita es orientación; el hook es lo que la sostiene. Por eso el
enforcement va en git y no en el agente: funciona con cualquier herramienta,
presente o futura, e incluso cuando el que rompe la regla sos vos.

### 3. Lo que se afirma de una fuente se verifica contra la fuente

`scripts/verify_citations.py` comprueba que cada afirmación de un deck sobre un
paper aparezca **textualmente** en el paper. Las citas se validan como
substring exacto tras normalizar espacios y énfasis markdown.

Las ecuaciones van en un carril aparte, porque la conversión PDF→markdown las
destroza: se transcriben, se marcan y se listan para chequeo humano. Y
`NOT-REPORTED` es una salida válida — sin esa escotilla, la sección de
limitaciones se inventa sola.

## Verificadores

```bash
python .agent/scripts/verify_citations.py <deck>/slides.md
python .agent/scripts/ingest_paper.py --check Papers/Papers_Markdown
python .agent/scripts/check_frozen.py --list
```

Sólo biblioteca estándar. Sin instalar nada.

## Probar que los verificadores sirven

Una vez por proyecto, rompé algo a propósito y confirmá que falla: cambiá una
palabra de una cita, o tocá un archivo bajo un directorio congelado.

Un verificador que nunca viste fallar no te está protegiendo de nada.

## Origen

Las ideas de estados ACTIVE/FROZEN, escalera de confianza, handoffs y el campo
Sorpresa vienen de
[ai-workspace-framework-core](https://github.com/matiaszaldarriaga/ai-workspace-framework-core),
de Matías Zaldarriaga (IAS Princeton). Esta versión las reduce a lo aplicable a
trabajo individual, agrega los verificadores mecánicos y el pipeline de papers,
y saca todo lo específico de la infraestructura de cómputo del IAS.
