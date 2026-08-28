# Nota de lectura de un paper

Nota estructurada y breve de un paper, para poder citarlo después sin volver a
leerlo entero. Complementa a `paper-slides.md`: la nota es para vos, el deck es
para entender y explicar.

## Parámetros

- `{fuente}` — ruta al `.md` del paper

## Regla

Vale la misma regla que en `paper-slides.md`: **lo que se afirma del paper se
respalda con texto del paper**. Las citas van entre comillas y textuales.

La diferencia es que la nota **sí** mezcla lectura propia con lo citado, pero
en secciones separadas y rotuladas.

## Formato

```markdown
# <Autor> <Año> — <Título>

**Clave BibTeX:** lee1994classification
**Fuente:** `Papers/Papers_Markdown/<archivo>.md`
**Leído:** <fecha>

## En una frase
Qué hace el paper.

## Problema
Qué motiva el trabajo.

## Método
Cómo lo resuelve. Las ecuaciones centrales transcritas, marcadas como
transcritas.

## Resultados
Los números que importan, copiados tal como aparecen.

## Limitaciones
Lo que el paper reconoce. Si no reconoce ninguna: "el paper no las reporta".

## Qué me sirve
Lectura propia: cómo se conecta con el trabajo. Esta sección NO se cita
porque no es del paper.

## Qué no me sirve
Por qué partes de este trabajo no aplican a mi caso.

## Citas guardadas
> "texto textual que voy a querer citar en la tesis"
```

## Reglas

**Los números se copian, no se redondean.** `95·8%` va como está, con el
separador raro del OCR incluido. Ya lo vas a limpiar al escribir la tesis;
mientras tanto querés poder verificarlo.

**"Qué no me sirve" no es opcional.** Obliga a leer críticamente en vez de
resumir. Es la sección que después evita citar un paper para algo que en
realidad no sostiene.

**Si la conversión está rota, se para.** Un `.md` vacío o truncado no se
compensa con lo que ya sabías del tema. Verificalo con:

```bash
python .agent/scripts/ingest_paper.py --check Papers/Papers_Markdown
```

## Salida

`Papers/notas/<id>.md`, con el mismo `<id>` corto y estable que usan los decks.
