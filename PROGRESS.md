# research-core — estado de construccion

Ultima actualizacion: 2026-08-28

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
- [ ] `AGENTS.md`
- [ ] `rules/CONTRACT.md` — modos, stop rules, evidencia sobre explicacion
- [ ] `rules/LAYOUT.md` — ACTIVE/FROZEN, escalera de confianza, promocion
- [ ] `workflows/sanity-check.md` — controles anti-autoengano en ML
- [ ] `workflows/provenance.md` — figura -> script + datos + commit + seed
- [ ] `workflows/experiment-log.md` — con campo Surprise
- [ ] `workflows/interpret-results.md` — plot-first
- [ ] `workflows/handoff.md`
- [ ] `workflows/discuss.md`
- [ ] `workflows/plan.md`
- [ ] `workflows/paper-note.md`
- [ ] `scripts/check_frozen.py` + `hooks/pre-commit`
- [ ] `adapters/` (claude, cursor, generic) + `install.py`

### Fase C — instalacion
- [ ] Instalar en `Tesis-Sammy`
- [ ] Commit inicial en ambos repos

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
