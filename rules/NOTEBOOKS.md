# Notebooks

## El problema

Un `.ipynb` es JSON con el código escapado dentro de arrays de strings, y con
las salidas —incluidas las imágenes en base64— embebidas en el mismo archivo.

Medido sobre notebooks reales de este tipo de trabajo, entre el **90% y el 99%
del archivo son salidas**, no código. Eso tiene tres consecuencias:

- **El diff de git es ilegible.** Reejecutar un notebook sin cambiar una línea
  produce un diff enorme.
- **Los conflictos de merge son casi irresolubles.**
- **Un agente que lee el notebook consume su contexto en base64** que no aporta
  nada. En un notebook grande puede directamente no entrar.

## La regla

**El texto plano es la fuente de verdad. El `.ipynb` es artefacto derivado.**

Para trabajo nuevo, un `.py` con celdas marcadas (`# %%`) suele alcanzar y es
lo más simple.

Para notebooks que ya existen y están en uso, **emparejar con Jupytext**:

```bash
pip install jupytext
jupytext --set-formats ipynb,py:percent codigos/mi_notebook.ipynb
```

Genera un `.py` espejado que se sincroniza al guardar. Seguís trabajando en
Jupyter o VS Code igual que antes; el `.py` es lo que se versiona, se revisa y
se edita programáticamente.

Costo de migración: cercano a cero. Por eso se prefiere a reescribir todo en
otra herramienta de notebooks en medio de un proyecto con fecha de entrega.

## Qué versionar

Versionar el `.py`. Para el `.ipynb`, dos opciones válidas:

- **Ignorarlo** en `.gitignore` — el más limpio.
- **Versionarlo limpio** con `nbstripout`, que borra las salidas antes de cada
  commit. Útil si querés que el notebook se abra directo desde el repo.

Versionar el `.ipynb` con salidas sólo se justifica si las figuras renderizadas
tienen que verse sin ejecutar nada. En ese caso es una decisión consciente, no
el estado por defecto.

Las figuras que importan no viven dentro del notebook: se guardan como archivos
en `docs/figuras/` o `runs/<id>/`, con su registro en `PROVENANCE.md`.

## Legibilidad

- Una celda hace una cosa.
- Las funciones reutilizables se van a `src/`. Un notebook con la misma función
  copiada tres veces ya es código que hay que promover.
- Las constantes mágicas van arriba y con nombre.
- El notebook tiene que correr de arriba a abajo en un kernel limpio. Si depende
  de haber ejecutado celdas en cierto orden, está roto aunque hoy funcione.
