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

## Procedimiento

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
mdc: true
sources:
  autor1994: ../../Papers_Markdown/Autor et al. - 1994 - Titulo.md
---
```

Las rutas son relativas al archivo del deck. El id (`autor1994`) es el que se
usa en cada cita.

### 4. Sintaxis de citas

En el cuerpo de la diapositiva, cada afirmación lleva una marca `[^n]`.
En las notas del presentador de **esa misma diapositiva**, una entrada por marca:

```markdown
- El estimador Z es suficiente para la covarianza C[^1]
- La distancia se computa píxel a píxel[^2]

<!--
[^1] autor1994 :: Goodman showed that Z is the maximum likelihood estimator of, and a sufficient statistic for, the covariance C
[^2] autor1994 :: is computed for each class, and the class associated with the minimum distance is assigned to the pixel
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

### 10. Comprobar que el verificador sirve

Una vez por proyecto, corrompé una cita a propósito — cambiá una palabra por
otra — y confirmá que el verificador falla. Un verificador que nunca viste
fallar no te está protegiendo de nada.

## Previsualizar y exportar

```bash
npx @slidev/cli <destino>/slides.md          # servidor local
npx @slidev/cli export <destino>/slides.md   # PDF
```

La exportación a PDF necesita `playwright-chromium`, que se instala aparte:

```bash
npm i -D playwright-chromium
```

## Errores a evitar

- **Rellenar con conocimiento del campo.** Si sabés que un método suele dar 95%
  pero el paper no lo dice, no va.
- **Redondear o convertir números.** `95·8%` se cita como está.
- **Atribuir al paper la crítica de otro.** Un paper que cita una limitación
  ajena no la está reportando como propia.
- **Citar la sección de referencias.** El texto existe en la fuente y pasa el
  verificador, pero no respalda nada.
