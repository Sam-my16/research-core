"""Adaptador para Claude Code.

Claude Code lee `CLAUDE.md`, no `AGENTS.md`. La doc oficial recomienda
importar uno desde el otro para no duplicar contenido.

Se usa el import `@AGENTS.md` y no un symlink: en Windows crear un symlink
requiere Developer Mode o privilegios de administrador.
"""

NAME = "claude"

CONTENT = """@AGENTS.md

## Claude Code

Las reglas y workflows de este proyecto estan en `AGENTS.md`, importado arriba.
El contenido real vive en `.agent/`.

Los workflows se invocan diciendo "segui `.agent/workflows/<nombre>.md`".
"""


def apply(project_root, agent_dir, log):
    target = project_root / "CLAUDE.md"
    if target.exists():
        existing = target.read_text(encoding="utf-8")
        if "@AGENTS.md" in existing:
            log("CLAUDE.md ya importa AGENTS.md, sin cambios")
            return
        target.write_text("@AGENTS.md\n\n" + existing, encoding="utf-8")
        log("CLAUDE.md: se antepuso el import de AGENTS.md")
        return
    target.write_text(CONTENT, encoding="utf-8")
    log("CLAUDE.md creado (una linea de import)")
