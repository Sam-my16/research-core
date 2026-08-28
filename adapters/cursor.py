"""Adaptador para Cursor.

Cursor lee `AGENTS.md` de forma nativa, asi que el adaptador solo agrega una
regla que apunta al contenido en `.agent/` para que aparezca en el panel de
reglas del editor.
"""

NAME = "cursor"

RULE = """---
description: Reglas y workflows de research-core
alwaysApply: true
---

# research-core

Las reglas de este proyecto estan en `AGENTS.md` y en `.agent/rules/`.

Antes de trabajar, leer:

- `.agent/rules/CONTRACT.md` — modos, cuando parar, evidencia antes que explicacion
- `.agent/rules/LAYOUT.md` — ACTIVE/FROZEN, escalera de confianza

Los workflows de `.agent/workflows/` se invocan por nombre.

Reglas duras:

- Nada bajo un directorio con archivo `FROZEN` se modifica.
- Un numero que solo esta en `explorations/` no es un resultado.
- No adivinar fechas: ejecutar `date +%Y-%m-%d_%H%M%S`.
- No hacer commit salvo pedido explicito.
"""


def apply(project_root, agent_dir, log):
    rules_dir = project_root / ".cursor" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    target = rules_dir / "research-core.mdc"
    target.write_text(RULE, encoding="utf-8")
    log(".cursor/rules/research-core.mdc escrito")
