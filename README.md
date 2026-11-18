# research-core

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-stdlib%20only-informational)

Un kit de reglas y chequeos automáticos para trabajar con asistentes de IA
(Claude, Cursor, Copilot, etc.) en un proyecto de investigación — una tesis,
un paper — sin que se cuele información inventada.

## El problema que resuelve

Los asistentes de IA son muy buenos armando resúmenes y presentaciones de
papers científicos. También inventan citas, cifras y resultados con total
seguridad, y a simple vista una cita falsa se ve igual que una real.

research-core agrega un paso de verificación automático: antes de confiar en
algo que el asistente escribió, un script compara cada cita, palabra por
palabra, contra el paper original.

## Ejemplo

Se tomó una presentación real y se le metieron a propósito cuatro errores
típicos de un asistente que alucina evidencia. El verificador los detectó
los cuatro:

| Error inyectado | Detectado |
|---|---|
| Una cifra inventada, sin nada parecido en la fuente | ✅ |
| Una cita real con una palabra cambiada | ✅ (y muestra el texto correcto al lado) |
| Una nota al pie sin su referencia | ✅ |
| Una cita a una fuente no declarada | ✅ |

El objetivo no es confiar en el asistente: es poder comprobarlo.

## Cómo funciona

- Se instala con un solo comando dentro de cualquier proyecto de
  investigación, sin depender de internet ni de paquetes externos.
- Define reglas simples (cuándo preguntar, cuándo no inventar, cuándo
  verificar) que funcionan con cualquier asistente de IA.
- Protege los resultados ya usados en la tesis: una vez que un número entra
  al documento final, el archivo que lo generó queda "congelado" y no se
  puede tocar por error.
- Verifica automáticamente que las citas, cifras y afirmaciones de cada
  presentación existan de verdad en el paper original.

## Instalar

```bash
python install.py /ruta/al/proyecto --tools claude
```

## Origen

Las ideas de base vienen de
[ai-workspace-framework-core](https://github.com/matiaszaldarriaga/ai-workspace-framework-core),
de Matías Zaldarriaga (IAS Princeton), adaptadas aquí para trabajo individual
y con los verificadores automáticos agregados.

## Licencia

[MIT](LICENSE).
