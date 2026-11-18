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
---
tags: [paper]
---

# <Autor> <Año> — <Título>

**Clave BibTeX:** lee1994classification
**Fuente:** `Papers/Papers_Markdown/<archivo>.md`
**Leído:** <fecha>
**Conceptos relacionados:** [[nombre-del-concepto]], [[otro-concepto]]

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

## Referencias bibliográficas

Cuando extraigas o normalices las referencias de un paper:

1. **Nunca completes un dato faltante.** Si una referencia está incompleta —sin
   año, sin DOI, con autores truncados por mal parseo del PDF— marcala como
   `[dato faltante: revisar manualmente]`. Un año inventado en una bibliografía
   es indetectable después y sobrevive hasta la versión impresa.
2. **Señalá los duplicados, no los fusiones.** Si dos referencias parecen el
   mismo trabajo con formato o datos distintos, marcalo como posible duplicado
   y preguntá antes de unificarlas.
3. **Identificá el estilo antes de convertir.** Los papers mezclan estilos entre
   sí y a veces dentro del mismo paper. Si no se puede determinar, decilo.
4. Entregá la lista normalizada y, **por separado**, las advertencias que
   requieren revisión manual. Mezclarlas hace que nadie revise nada.

## Salida

`Papers/notas/<id>.md`, con el mismo `<id>` corto y estable que usan los decks.

## Compatibilidad con Obsidian (opcional)

Las notas son markdown plano: abrir `Papers/` como vault en Obsidian (File →
Open folder as vault) da grafo y backlinks sin configurar nada más.

- **Reusá el nombre exacto de un concepto** en `Conceptos relacionados` cuando
  vuelva a aparecer en otra nota — `[[wishart-distribution]]`, no
  `[[distribución wishart]]` en una nota y `[[dist. Wishart]]` en otra. Dos
  nombres distintos para lo mismo no se conectan en el grafo.
- No hace falta crear `Papers/notas/` de antemano: aparece sola cuando se
  guarda la primera nota. Un directorio vacío es ruido (ver `LAYOUT.md`).
- El grafo es para pensar, no es evidencia: lo que se cita en la tesis sigue
  siendo lo que pasa por `verify_citations.py`, no un link de Obsidian.
