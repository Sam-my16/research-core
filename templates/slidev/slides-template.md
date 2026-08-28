---
theme: default
title: "AUTOR AÑO — Título corto"
info: |
  Deck explicativo generado bajo el contrato de citas de research-core.
  Verificar con: python .agent/scripts/verify_citations.py slides.md
class: text-left
transition: slide-left
sources:
  SOURCEID: ../../Papers_Markdown/NOMBRE-DEL-ARCHIVO.md
---

# Título del paper

**Autores (Año)** · *Publicación*

---

## El problema

- Afirmación respaldada[1]

<!--
[1] SOURCEID :: cita textual exacta copiada del .md fuente
-->

---

## El aporte central

- Afirmación respaldada[1]

<!--
[1] SOURCEID :: cita textual exacta
-->

---

## Ecuación clave

$$
d(Z, \omega_m) = n\left[\ln|C_m| + \mathrm{Tr}\!\left(C_m^{-1} Z\right)\right] - \ln\!\left[P(\omega_m)\right]
$$

<div class="text-sm opacity-60 mt-2">
Ecuación <strong>transcrita</strong>, no verificada automáticamente[1].
Contrastar contra el PDF antes de citarla en la tesis.
</div>

<!--
[1] SOURCEID :: EQ
-->

---

## Qué funcionó

- Resultado positivo con su número citado[1]

<!--
[1] SOURCEID :: cita textual con el número tal como aparece
-->

---

## Qué no funcionó

- Limitación explícita del paper[1]

<div class="mt-4 text-xs opacity-60">
El paper no reporta ASPECTO[2].
</div>

<!--
[1] SOURCEID :: cita textual de la limitación
[2] SOURCEID :: NOT-REPORTED
-->

---

## Relevancia para el trabajo propio

<div class="mt-6 p-4 border-l-4 border-blue-400 bg-blue-50 dark:bg-blue-900/20 text-sm">
<strong>Lectura propia:</strong> conexión con la tesis.
Este bloque es interpretación, no del paper — por eso no lleva cita.
</div>

<style>
.slidev-layout { font-size: 0.95rem; }
sup { opacity: 0.5; font-size: 0.7em; }
</style>
