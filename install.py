#!/usr/bin/env python3
"""Instala research-core dentro de un proyecto.

Copia el contenido neutro a `<proyecto>/.agent/`, genera `AGENTS.md` y aplica
los adaptadores de las herramientas que uses.

Se copia en vez de usar submodulo o symlink por tres motivos:

  - el proyecto queda autocontenido: el dia que entregues o publiques la tesis,
    las reglas viajan adentro y se leen sin depender de otro repo
  - los symlinks en Windows requieren Developer Mode
  - los submodulos son friccion pura para trabajo individual

`.agent/VERSION` deja registrado desde que commit se copio, para saber cuando
hay que actualizar.

Uso:
    python install.py <proyecto>
    python install.py <proyecto> --tools claude,cursor
    python install.py <proyecto> --update
"""

import argparse
import importlib.util
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CORE = Path(__file__).resolve().parent
COPIED = ["rules", "workflows", "templates", "scripts", "hooks"]
BLOCK_START = "<!-- research-core:inicio"
BLOCK_END = "<!-- research-core:fin -->"


for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def log(msg):
    print("  " + msg)


def core_version():
    try:
        out = subprocess.run(
            ["git", "-C", str(CORE), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "desconocido"


def copy_content(agent_dir, update):
    if agent_dir.exists() and not update:
        print("ERROR: ya existe {}".format(agent_dir), file=sys.stderr)
        print("       usa --update para actualizarlo", file=sys.stderr)
        return False

    for name in COPIED:
        src = CORE / name
        if not src.is_dir():
            continue
        dst = agent_dir / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        log("{}/ copiado ({} archivos)".format(name, len(list(dst.rglob("*")))))

    version = core_version()
    (agent_dir / "VERSION").write_text(
        "research-core {}\ninstalado {}\n".format(
            version, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),
        encoding="utf-8",
    )
    log("VERSION: {}".format(version))
    return True


def write_agents_md(project_root, agent_dir):
    """Genera AGENTS.md respetando lo que el usuario haya escrito.

    El bloque delimitado se regenera; todo lo de afuera se conserva.
    """
    template = (CORE / "templates" / "AGENTS.md").read_text(encoding="utf-8")
    rendered = template.replace("{PROJECT_NAME}", project_root.name)
    target = project_root / "AGENTS.md"

    if not target.exists():
        target.write_text(rendered, encoding="utf-8")
        log("AGENTS.md creado")
        return

    existing = target.read_text(encoding="utf-8")
    if BLOCK_START not in existing or BLOCK_END not in existing:
        log("AGENTS.md ya existe y no tiene el bloque de research-core; se deja intacto")
        log("   -> agregale a mano: 'Ver .agent/rules/ y .agent/workflows/'")
        return

    new_block = rendered[rendered.index(BLOCK_START):rendered.index(BLOCK_END) + len(BLOCK_END)]
    head = existing[:existing.index(BLOCK_START)]
    tail = existing[existing.index(BLOCK_END) + len(BLOCK_END):]
    target.write_text(head + new_block + tail, encoding="utf-8")
    log("AGENTS.md: bloque de research-core actualizado, el resto intacto")


def install_hooks(project_root, agent_dir):
    hooks = agent_dir / "hooks"
    if not hooks.is_dir():
        return
    for hook in hooks.iterdir():
        if hook.is_file():
            hook.chmod(0o755)
    try:
        subprocess.run(
            ["git", "-C", str(project_root), "config", "core.hooksPath", ".agent/hooks"],
            check=True, capture_output=True, text=True,
        )
        log("core.hooksPath -> .agent/hooks")
        log("   OJO: esto vive en .git/config y NO se clona.")
        log("   En cada clon nuevo: git config core.hooksPath .agent/hooks")
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        log("aviso: no se pudo configurar core.hooksPath ({})".format(exc))


def load_adapter(name):
    path = CORE / "adapters" / "{}.py".format(name)
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location("adapter_" + name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    ap = argparse.ArgumentParser(description="Instalar research-core en un proyecto.")
    ap.add_argument("project", type=Path, help="directorio del proyecto")
    ap.add_argument("--tools", default="claude",
                    help="adaptadores separados por coma (claude,cursor,generic)")
    ap.add_argument("--update", action="store_true",
                    help="actualizar una instalacion existente")
    args = ap.parse_args()

    project_root = args.project.resolve()
    if not project_root.is_dir():
        print("ERROR: no existe {}".format(project_root), file=sys.stderr)
        return 2

    agent_dir = project_root / ".agent"
    print("Instalando research-core en {}".format(project_root))
    print()

    if not copy_content(agent_dir, args.update):
        return 1
    write_agents_md(project_root, agent_dir)
    install_hooks(project_root, agent_dir)

    for name in [t.strip() for t in args.tools.split(",") if t.strip()]:
        adapter = load_adapter(name)
        if adapter is None:
            log("aviso: no existe el adaptador '{}'".format(name))
            continue
        adapter.apply(project_root, agent_dir, log)

    print()
    print("Listo. Proximos pasos:")
    print("  - revisar AGENTS.md y agregar lo especifico del proyecto al final")
    print("  - versionar .agent/ (para que las reglas viajen con el repo)")
    print("  - comprobar el hook: python .agent/scripts/check_frozen.py --list")
    return 0


if __name__ == "__main__":
    sys.exit(main())
