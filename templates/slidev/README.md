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
npx @slidev/cli export Papers/decks/<id>/slides.md
```

`npx` evita tener que instalar Slidev por deck. La exportación a PDF necesita
`playwright-chromium` aparte:

```bash
npm i -D playwright-chromium
```

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
[^3] cita NO encontrada literalmente en 'lee1994':
     buscado: "four-look SA R data is slightly better in classification..."
     lo mas parecido en la fuente: "...ok sa r data is much better in classification..."
```

Si dice `no hay nada parecido en la fuente`, la afirmación fue inventada.

## Probar que el verificador funciona

Una vez por proyecto: cambiá una palabra de una cita que pasa, corré el
verificador y confirmá que falla. Después revertí el cambio.

Un verificador que nunca viste fallar no te está protegiendo de nada.
