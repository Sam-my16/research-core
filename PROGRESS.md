# research-core — estado de construccion

Ultima actualizacion: 2026-08-29

## Decisiones de diseno (cerradas)

1. **Contenido neutro, adaptadores descartables.** Ningun archivo de `rules/` o
   `workflows/` menciona una herramienta. `AGENTS.md` es la entrada estandar;
   `CLAUDE.md` es una linea (`@AGENTS.md`). Cambiar de herramienta = reescribir
   un adaptador de ~30 lineas, no el contenido.
2. **Distribucion por copia, no submodulo ni clon anidado.** `install.py` copia
   a `<proyecto>/.agent/` y estampa el commit en `.agent/VERSION`.
   El proyecto queda autocontenido.
3. **Citas verificadas por texto literal, no por numero de linea.** Un rango de
   lineas "que existe" no prueba nada y se rompe al reconvertir el PDF.
4. **Ecuaciones en carril aparte** (`EQ`): transcritas a LaTeX, excluidas de la
   verificacion automatica, listadas en el reporte para chequeo humano.
   Motivo: markitdown destroza las formulas (verificado sobre Lee 1994).
5. **`NOT-REPORTED` es salida valida y esperada.** Los papers rara vez enuncian
   sus fracasos; sin escotilla explicita el modelo los inventa.
6. **Enforcement por `core.hooksPath`** apuntando a un directorio versionado.
   `.git/hooks/` NO viaja con el clon.
7. **Python, no bash.** El framework original dependia de bash + symlinks, las
   dos cosas fragiles en Windows.

## Tareas

### Fase A — pipeline de papers (probarlo antes de escribir el resto)
- [x] Esqueleto del repo + git init
- [x] `scripts/verify_citations.py` — verificador de citas literales
- [x] `workflows/paper-slides.md` — el contrato de como se arma un deck
- [x] `templates/slidev/` — plantilla, estilos, README
- [x] Deck real de prueba: Lee et al. 1994
- [x] **Probar que el verificador FALLA con un deck corrompido a proposito**
      Resultado: 4/4 defectos detectados, exit code 1. Ver "Evidencia" abajo.

### Fase B — framework
- [x] `AGENTS.md`
- [x] `rules/CONTRACT.md` — modos, stop rules, evidencia sobre explicacion
- [x] `rules/LAYOUT.md` — ACTIVE/FROZEN, escalera de confianza, promocion
- [x] `workflows/sanity-check.md` — controles anti-autoengano en ML
- [x] `workflows/provenance.md` — figura -> script + datos + commit + seed
- [x] `workflows/experiment-log.md` — con campo Surprise
- [x] `workflows/interpret-results.md` — plot-first
- [x] `workflows/handoff.md`
- [x] `workflows/discuss.md`
- [x] `workflows/plan.md`
- [x] `workflows/paper-note.md`
- [x] `scripts/check_frozen.py` + `hooks/pre-commit`
- [x] `adapters/` (claude, cursor, generic) + `install.py`

### Fase C — instalacion
- [x] Instalar en `Tesis-Sammy`
- [x] `scripts/export_deck.py` — un solo comando para exportar (research-core 943b476)
- [x] `--update` de Tesis-Sammy a 943b476: `.agent/scripts` tiene 4 verificadores
- [ ] Commit en Tesis-Sammy  <- PENDIENTE, requiere decision del usuario
      Hay un commit acotado disponible y limpio:
        Papers/decks/barrachina2023-comparison/  (nuevo)
        Papers/decks/xie2017/                    (nuevo)
        Papers/decks/lee1994/lee1994.pdf         (reexportado)
        .agent/                                  (actualizado a 943b476)
      NO tocar `codigos/`: los borrados y `codigos/SAR/` son el movimiento de
      archivos a medio terminar que ya estaba ahi antes de esta instalacion.

## Notas del entorno (verificadas)

- Python 3.11.15, Node v22.23.2, git 2.47.0 — OK
- `markitdown` NO instalado. No es bloqueante: `Papers/Papers_Markdown/` ya
  tiene 11 papers convertidos y esos son el input real del pipeline.
- Dos fuentes rotas en `Papers_Markdown/`: `H_A_alpha_Polarimetric_Decomposition.md`
  y `H_A_alpha_Polarimetric_Decomposition.pdf.md`, ambas de 0 bytes.
- Nombres inconsistentes: `Ferro-Famil ... .pdf.md` (doble extension).
  El verificador debe tolerarlo (fuentes declaradas por ruta explicita).
- Exportar Slidev a PDF requiere `playwright-chromium` aparte de npm.


## Evidencia — Fase A

Deck real: `Tesis-Sammy/Papers/decks/lee1994/slides.md` (10 diapositivas).

Verificacion sobre el deck limpio:

    citas verificadas literalmente : 25
    ecuaciones transcritas         : 1  (chequeo humano)
    marcado como no reportado      : 1
    errores                        : 0
    RESULTADO: OK

Prueba negativa — se inyectaron 4 defectos a proposito y el verificador
detecto los 4 (exit code 1):

1. Afirmacion inventada con cifra plausible ("98.7% de exactitud global")
   -> "no hay nada parecido en la fuente"
2. Cita real alterada en UNA palabra (much -> slightly)
   -> detectada, y el reporte mostro el texto verdadero al lado
3. Marca [^9] usada sin entrada en las notas -> detectada
4. Cita a una fuente no declarada en el frontmatter -> detectada

Auditoria de fuentes (`ingest_paper.py --check`): 13 archivos, 11 OK, 2 rotos
(`H_A_alpha_Polarimetric_Decomposition.md` y `.pdf.md`, ambos 0 bytes).
Esos dos no pueden usarse como fuente hasta reconvertirlos.


## Evidencia — Fase B y C

Instalacion en `Tesis-Sammy` (research-core a3a22eb):
`.agent/` con rules(3) workflows(9) templates(4) scripts(3) hooks(1),
`AGENTS.md`, `CLAUDE.md` (una linea de import), `core.hooksPath -> .agent/hooks`.

**Prueba del hook de FROZEN, sobre el repo real de la tesis:**
se creo `runs/_hooktest/` con un archivo y un marcador `FROZEN`, y se intento
commitear una modificacion. Resultado: commit BLOQUEADO, HEAD sin cambios.
El propio archivo `FROZEN` no fue señalado, que es lo correcto: crearlo es el
acto de congelar. Prueba limpiada despues.

## Pendiente / decisiones abiertas

- El repo `Tesis-Sammy` tiene cambios previos sin commitear que NO son de esta
  instalacion: `codigos/process.ipynb`, `codigos/sar_preprocess.py` e
  `image.png` figuran borrados, y `codigos/SAR/` esta sin trackear. Parece un
  movimiento de archivos a medio terminar. No se tocaron.
- `jupytext` no esta instalado. Ver `rules/NOTEBOOKS.md`: los notebooks actuales
  son 90-99% salidas embebidas.
- Dos fuentes en `Papers_Markdown/` siguen rotas (0 bytes).
- Faltan decks para 8 papers (hechos: lee1994, barrachina2023-comparison,
  xie2017).
- Archivos sueltos en `Papers/decks/`: `_check_quotes.py` y `_q.txt` son
  andamiaje de sesion y se pueden borrar. `render_decks.py` se superpone con
  `export_deck.py` (exporta todos los decks de una vs. uno solo con
  `--install-deps`): decidir cual sobrevive antes de commitear.


## Correcciones tras revision (commit e893005)

Tres afirmaciones que estaban escritas y eran falsas:

1. **"El hook viaja con el repo"** — falso. `core.hooksPath` se guarda en
   `.git/config`, que no se clona. Verificado clonando Tesis-Sammy: el clon
   no tiene hooksPath configurado. El archivo del hook si viaja, pero queda
   desarmado. Corregido en README, hooks/pre-commit e install.py, y agregado
   el paso de armado a la documentacion.

2. **Las marcas de cita se rompian al renderizar.** Solo se ve exportando:
   - `[^n]` (nota al pie de markdown) -> superindice: `q = 3^4`, se lee potencia
   - `[n]` con `mdc: true` -> pierde corchetes: `q = 3[4]` queda `q = 34`
   La combinacion correcta es `[n]` sin `mdc`. Probado con las cuatro variantes
   en un deck de prueba y verificado en PDF.

3. **El verificador prometia mas de lo que hace.** Prueba que la cita es real,
   no que respalde la afirmacion a la que esta pegada. Limite ahora documentado
   en README y en workflows/paper-slides.md.

Ademas: `install.py --update` probado (regenera el bloque de AGENTS.md y
conserva lo escrito afuera), y las diapositivas con frontmatter propio ya no
desplazan la numeracion de los errores.

## Hallazgos sobre el entorno de la tesis

- **Nombres de archivo demasiado largos.** Clonar Tesis-Sammy falla con
  `Filename too long` en varios papers: superan el limite de 260 caracteres de
  Windows. Se arregla con `git config --global core.longpaths true`.
- **Notebooks: 90-99% del archivo son salidas embebidas.** CAE_CVAE_DTD.ipynb
  son 955 KB de los cuales 20 KB es codigo. Ver rules/NOTEBOOKS.md.
- El export de Slidev a PDF necesita DOS pasos: `npm i -D playwright-chromium`
  y ademas `npx playwright install chromium`.


## Evidencia — decks (2026-08-29)

Tres decks pasan el verificador, exit 0:

    lee1994                    32 citas literales, 1 EQ, 1 NOT-REPORTED, 0 errores
    barrachina2023-comparison  61 citas literales, 2 EQ, 1 NOT-REPORTED, 0 errores
    xie2017                    53 citas literales, 6 EQ, 1 NOT-REPORTED, 0 errores

Los avisos son el limite conocido del verificador, no fallas suyas: senalan
vinetas sin cita. El que importa revisar a mano es **barrachina, diapositiva
11** — los margenes complejo−real (+0.84 / +0.13 / +0.32 OA) son aritmetica
derivada de la tabla, no algo que el paper enuncie. El verificador no puede
verlo: comprueba que una cita sea real, no que respalde la afirmacion.

## Correcciones al diff de Antigravity (commit 943b476)

1. `export_deck.py` llamaba `subprocess.run(["npx", ...])` sin resolver el
   ejecutable. En Windows los lanzadores de Node son `.cmd` y CreateProcess no
   agrega la extension: fallaba siempre con "npx no esta disponible" aunque
   Node estuviera instalado. Y como los dos documentos ya apuntaban al script,
   la ruta de exportacion documentada quedaba muerta. Resuelto con
   `shutil.which("npx.cmd")`, no con `shell=True` (las rutas tienen espacios).
2. `--install-deps` corria `npm i -D` en el cwd, no en el directorio del deck.
   Corregido con `cwd=`.
3. Se revirtio el hunk de `adapters/claude.py` que corria `npx skills add`
   en cada instalacion: la skill es por usuario (`-g`), el adaptador corre por
   proyecto. Sin `-g` deja `.agents/skills/`, un symlink y `skills-lock.json`
   dentro del repo del usuario. Ademas iba sin `-y`, con `capture_output=True`
   y sin `timeout`: un instalador de codigo de terceros, en silencio y colgable.
4. `CHANGES_FOR_CLAUDE.md` afirma que Slidev publico "un servidor MCP (Skill)".
   Son dos cosas: `npx skills add` instala una **skill** (archivos de sintaxis);
   el **MCP** vive en `localhost:3030/__mcp` y solo existe con el dev server
   levantado.
