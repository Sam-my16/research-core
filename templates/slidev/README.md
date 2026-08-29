# Decks de papers con Slidev

Sistema para convertir un paper en diapositivas explicativas donde **cada
afirmación está respaldada por una cita textual verificable**.

El contrato completo está en `workflows/paper-slides.md`. Esto es la referencia
operativa.

## Flujo

```
paper.pdf  ──(markitdown)──>  paper.md  ──(agente)──>  slides.md
                                  │                        │
                                  └────── verificador ─────┘
```

La conversión es opcional: si ya tenés los `.md`, son el input real.

## Comandos

Auditar conversiones existentes (detecta archivos vacíos o truncados):

```bash
python .agent/scripts/ingest_paper.py --check Papers/Papers_Markdown
```

Convertir un PDF nuevo:

```bash
pip install markitdown[pdf]
python .agent/scripts/ingest_paper.py Papers/nuevo.pdf -o Papers/Papers_Markdown
```

Verificar un deck (obligatorio antes de darlo por terminado):

```bash
python .agent/scripts/verify_citations.py Papers/decks/<id>/slides.md
```

Previsualizar y exportar:

```bash
npx @slidev/cli Papers/decks/<id>/slides.md
python .agent/scripts/export_deck.py Papers/decks/<id>/slides.md
```

`npx` evita tener que instalar Slidev por deck. La exportación a PDF necesita
Playwright, que podés instalar desde el mismo script si te falla:

```bash
python .agent/scripts/export_deck.py Papers/decks/<id>/slides.md --install-deps
```

## Ayudas de sintaxis (opcionales, se instalan una vez)

Cubren **cómo se escribe** una diapositiva. No reemplazan al verificador: el
contrato de qué puede decir el deck sigue en `workflows/paper-slides.md`.

**Skill de Slidev** — la referencia de sintaxis (layouts, animaciones, columnas,
resaltado de código, exportación) queda disponible para el agente:

```bash
npx skills add slidevjs/slidev -g --copy -y -a claude-code -a codex
```

Es una instalación **por usuario**, no por proyecto: el `-g`. Sin él se
instalan copias en cada repo y ensucian el árbol de trabajo. Una skill corre con
los permisos del agente, así que leela antes de usarla.

**Extensión de VS Code** — previsualización del deck al lado del editor:

```bash
code --install-extension antfu.slidev
```

**Servidor MCP** — deja que el agente inspeccione el deck que se está
renderizando:

```bash
claude mcp add --transport http --scope user slidev http://localhost:3030/__mcp
```

Sólo conecta mientras el servidor de desarrollo está levantado
(`npx @slidev/cli <deck>/slides.md`). Con el deck apagado, `claude mcp list`
muestra `ConnectionRefused`: eso es lo esperado, no una instalación rota.

## Convención de directorios

```
Papers/
├── *.pdf                  # originales
├── Papers_Markdown/       # conversiones (fuentes de verdad para las citas)
└── decks/
    └── <id>/
        └── slides.md
```

El `<id>` es corto y estable: `lee1994`, `zhang2017`, `barrachina2023-impact`.

## Leer el reporte del verificador

```
citas verificadas literalmente : 25    <- respaldadas, exactas
ecuaciones transcritas         : 1     <- requieren TU chequeo contra el PDF
marcado como no reportado      : 1     <- el paper no lo dice; es válido
errores                        : 0
avisos                         : 2
```

**Errores** bloquean. **Avisos** se revisan de a uno: una viñeta de
interpretación propia sin cita genera aviso y está bien; una afirmación sobre
el paper sin cita es un problema real.

Cuando una cita falla, el reporte muestra el fragmento más parecido de la
fuente al lado. Si el texto verdadero aparece ahí con una palabra distinta,
alguien alteró la cita:

```
[3] cita NO encontrada literalmente en 'lee1994':
     buscado: "four-look SA R data is slightly better in classification..."
     lo mas parecido en la fuente: "...ok sa r data is much better in classification..."
```

Si dice `no hay nada parecido en la fuente`, la afirmación fue inventada.

## Probar que el verificador funciona

Una vez por proyecto: cambiá una palabra de una cita que pasa, corré el
verificador y confirmá que falla. Después revertí el cambio.

Un verificador que nunca viste fallar no te está protegiendo de nada.
