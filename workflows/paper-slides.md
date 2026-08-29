# Generar diapositivas explicativas de un paper

Convertir un paper en un deck que permita entenderlo: ideas principales,
ecuaciones, qué funcionó y qué no. **Todo citado del paper, sin inventar nada.**

## Parámetros

- `{fuente}` — ruta al `.md` del paper (salida de la conversión PDF→markdown)
- `{destino}` — directorio del deck (por convención `Papers/decks/<id>/`)

## Regla dura

> Toda afirmación factual sobre el paper lleva una cita textual exacta del `.md`
> fuente. Si no podés respaldarla con texto literal, no va al deck.

Esto no es una recomendación de estilo: hay un verificador que lo comprueba
mecánicamente y falla si una cita no aparece literalmente en la fuente.

## La sintaxis no es el trabajo

Hay una skill de Slidev instalada a nivel de usuario: layouts, animaciones,
columnas, resaltado de código, exportación. Cubre **cómo se escribe** una
diapositiva y nada más.

Este workflow cubre **qué puede decir**. Son capas distintas y la de acá manda:
una diapositiva impecable con una afirmación sin cita no pasa el verificador. Si
el agente ya no gasta turnos peleando con el formato, ese tiempo va a lo que sí
hay que revisar.

Instalación y detalle operativo en `templates/slidev/README.md`.

## Procedimiento

### 0. Auditar la fuente contra el PDF — antes que nada

```bash
python .agent/scripts/ingest_paper.py --check Papers/Papers_Markdown
```

No empieces si el paper sale `PARCIAL`, `ROTO` o `SCAN`. Reconvertilo primero:

```bash
python .agent/scripts/ingest_paper.py "Papers/Autor 1994 - Titulo.pdf" -o Papers/Papers_Markdown --force
```

**Este paso no es burocracia; tapa el único agujero que el verificador de citas
no puede ver.** El verificador comprueba las citas contra el `.md`. Nadie
comprueba el `.md` contra el PDF. Si el conversor se comió la sección de
limitaciones, el deck concluye *"el paper no reporta fallas"* y **todas sus
citas verifican limpias**, porque salieron de ese archivo.

No es hipotético. Le pasó al primer deck de este repo: markitdown recuperó el
39% de Lee 1994 y el deck perdió cuatro resultados negativos explícitos, entre
ellos *"the increase in dimensionality prevents efficient computation"* y
*"at the expense of a poorer classification of the coastal 'ocean' pixels"*.
El deck pasó 25/25 igual.

### 1. Leer la fuente entera antes de escribir nada

No escribas la primera diapositiva hasta haber leído el paper completo. Un deck
armado mientras leés termina siendo un resumen de la introducción.

Si el `.md` está vacío o truncado, **pará y avisá**. Una conversión rota no se
compensa con conocimiento previo del tema — ese es exactamente el camino por el
que se cuela la invención.

### 2. Recolectar las citas primero, redactar después

Extraé los pasajes literales que vas a usar y recién entonces escribí las
viñetas que resumen cada uno. Al revés (redactar y después buscar respaldo) el
resultado se parece a lo que ya creías del paper, no a lo que el paper dice.

### 3. Escribir el deck

Frontmatter con las fuentes declaradas:

```yaml
---
theme: default
title: "Autor Año — Título corto"
sources:
  autor1994: ../../Papers_Markdown/Autor et al. - 1994 - Titulo.md
---
```

**No pongas `mdc: true`.** Con MDC activado, Slidev interpreta `[4]` como
sintaxis de componente inline y se come los corchetes: `q = 3[4]` se renderiza
como `q = 34`, que se lee como treinta y cuatro. Verificado exportando a PDF.

Las rutas son relativas al archivo del deck. El id (`autor1994`) es el que se
usa en cada cita.

### 4. Sintaxis de citas

En el cuerpo de la diapositiva, cada afirmación lleva una marca `[n]`.
En las notas del presentador de **esa misma diapositiva**, una entrada por marca:

```markdown
- El estimador Z es suficiente para la covarianza C[1]
- La distancia se computa píxel a píxel[2]

<!--
[1] autor1994 :: Goodman showed that Z is the maximum likelihood estimator of, and a sufficient statistic for, the covariance C
[2] autor1994 :: is computed for each class, and the class associated with the minimum distance is assigned to the pixel
-->
```

Las citas viven en las notas y no en la diapositiva a propósito: la diapositiva
queda legible y, al presentar, tenés el respaldo textual delante.

**Copiá la cita tal cual está en el `.md`**, con sus errores de OCR incluidos
(`SA R`, `and'ridge'`, `95·8%`). El verificador normaliza espacios, énfasis
markdown y comillas tipográficas, pero no adivina palabras.

Elegí fragmentos de 40–150 caracteres. Muy cortos no son evidencia; muy largos
se rompen contra los saltos de página del OCR.

### 5. Los tres tipos de entrada

| Entrada | Significado | Verificación |
|---|---|---|
| `:: <texto literal>` | Afirmación respaldada | Substring exacto de la fuente |
| `:: EQ` | Ecuación transcrita a LaTeX | **Excluida**, se lista para chequeo humano |
| `:: NOT-REPORTED` | El paper no lo reporta | Ninguna; es una salida válida |

**Ecuaciones.** La conversión PDF→markdown destroza las fórmulas. Transcribilas
a LaTeX leyendo el original y marcalas `EQ`. Nunca las presentes con el mismo
aspecto visual que una afirmación verificada: llevan una nota que aclara que
requieren contraste contra el PDF.

**`NOT-REPORTED`.** Los papers rara vez enuncian sus fracasos. *"El paper no
reporta X"* es una respuesta correcta y esperada, no una falla del trabajo. Es
preferible una sección corta y honesta a una inventada.

### 6. Estructura recomendada

1. Portada — autores, publicación, año
2. El problema — qué motiva el trabajo
3. El aporte central — la idea en una diapositiva
4. Ecuaciones clave — transcritas, marcadas
5. Método — cómo se aplica
6. **Qué funcionó** — resultados positivos, con números citados
7. **Qué no funcionó** — ver abajo
8. Relevancia para el trabajo propio — interpretación, marcada como tal

### 7. "Qué no funcionó": de dónde sale

Sólo de estas cuatro fuentes dentro del paper:

- tablas de ablación y comparaciones donde una variante pierde
- secciones *Limitations* / *Discussion*
- *Future work* (lo que queda pendiente señala lo que no resolvieron)
- resultados negativos explícitos ("this approach is not feasible",
  "somewhat inferior to", "are ineffective in")

Si ninguna aporta nada, la sección dice que el paper no lo reporta y se acabó.

### 8. Interpretación propia

Está permitida y es útil — es la conexión con tu trabajo. Pero va en un bloque
visualmente distinto, **sin marca de cita**, y aclarando que es lectura propia.
El verificador avisará que esa viñeta no tiene cita; ese aviso es correcto y se
deja pasar conscientemente.

Nunca mezcles interpretación con afirmación citada en la misma viñeta.

### 9. Verificar (obligatorio antes de dar por terminado)

```bash
python .agent/scripts/verify_citations.py <destino>/slides.md
```

No entregues un deck que no pase. Los avisos se revisan uno por uno: algunos son
correctos (interpretación propia, texto estructural), otros señalan una
afirmación que se coló sin respaldo.

**Lo que el verificador no puede comprobar**, y son dos cosas distintas:

1. **Que la cita respalde la afirmación a la que está pegada.** Una cita
   verdadera bajo una viñeta que dice otra cosa pasa limpia. Eso lo comprobás
   vos al releer — por eso las citas viven en las notas del presentador.
2. **Que la fuente esté completa.** El verificador compara contra el `.md`, no
   contra el PDF. Eso lo cubre el paso 0, y sólo el paso 0.

### 9 bis. Elegir el formato de la fuente

Texto plano o markdown, nunca el PDF crudo como fuente citable. No es
preferencia: el verificador necesita un archivo de texto persistente para hacer
la comparación de substring. Sin él no queda ninguna garantía mecánica, y
además leer páginas de PDF como imágenes consume **más** tokens que el texto,
no menos.

**Cuidado con `pdftotext -layout`.** Preserva la posición horizontal, así que en
un paper a dos columnas lee las dos a la vez e intercala las líneas:

```
Commonly used deep learning algorithms include deep belief
image (usually converted to dB scale), while neglecting phase
```

Una cita copiada de ahí es una frase que no existe en el paper — y **pasa el
verificador**, porque sí está en el archivo fuente. Usá `pdftotext` sin
`-layout` (es lo que hace `ingest_paper.py`): su heurística de orden de lectura
resuelve bien las columnas.

Las ecuaciones son el caso donde el PDF sí gana, y para eso está el carril `EQ`:
abrí el PDF en las **páginas de las fórmulas solamente**, transcribí, marcá `EQ`.
Texto barato para la prosa, PDF dirigido para las fórmulas.

### 10. Comprobar que el verificador sirve

Una vez por proyecto, corrompé una cita a propósito — cambiá una palabra por
otra — y confirmá que el verificador falla. Un verificador que nunca viste
fallar no te está protegiendo de nada.

## Previsualizar y exportar

```bash
npx @slidev/cli <destino>/slides.md                       # servidor local
python .agent/scripts/export_deck.py <destino>/slides.md  # PDF
```

La exportación a PDF necesita el navegador de Playwright. Si nunca lo instalaste
y el export falla, podés instalar las dependencias con el mismo script:

```bash
python .agent/scripts/export_deck.py <destino>/slides.md --install-deps
```

Sin esas dependencias, el export falla con `Executable doesn't exist`.

**Mirá el deck renderizado antes de darlo por bueno.** Dos defectos reales que
sólo aparecen al exportar, ambos en la marca de cita pegada a un número:

- `[^4]` (nota al pie de markdown) se renderiza como `^4` — se lee como potencia.
- `[4]` con `mdc: true` se renderiza como `4` sin corchetes — `q = 3[4]` queda
  como `q = 34`.

La combinación correcta es `[4]` **sin** `mdc`. Verificar exportando, no
inspeccionando el HTML: en el HTML las marcas se ven bien en ambos casos.

## Errores a evitar

- **Rellenar con conocimiento del campo.** Si sabés que un método suele dar 95%
  pero el paper no lo dice, no va.
- **Redondear o convertir números.** `95·8%` se cita como está.
- **Atribuir al paper la crítica de otro.** Un paper que cita una limitación
  ajena no la está reportando como propia.
- **Citar la sección de referencias.** El texto existe en la fuente y pasa el
  verificador, pero no respalda nada.
