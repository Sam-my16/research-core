#!/usr/bin/env python3
"""Impide modificar artefactos congelados.

Un directorio se congela creando un archivo `FROZEN` adentro. Todo lo que
cuelga de el queda inmutable: se puede leer, copiar y citar, pero no modificar
ni volver a correr.

Motivo: cuando un numero entra en la tesis, el artefacto que lo produjo deja de
ser codigo de trabajo y pasa a ser evidencia. Si despues cambia -aunque sea
para mejorarlo- el numero deja de tener respaldo y nadie se entera.

Uso:
    python check_frozen.py              # revisa lo que esta en el indice (pre-commit)
    python check_frozen.py --worktree   # revisa tambien cambios sin agregar
    python check_frozen.py --list       # lista los directorios congelados
    python check_frozen.py <ruta>...    # revisa rutas concretas

Sale con codigo 1 si hay una violacion.
"""

import argparse
import subprocess
import sys
from pathlib import Path

MARKER = "FROZEN"


for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def repo_root():
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        )
        return Path(out.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def frozen_ancestor(path, root):
    """Devuelve el directorio congelado que contiene a `path`, o None.

    El propio archivo FROZEN no se considera congelado: crearlo es justamente
    el acto de congelar, y borrarlo es el acto deliberado de descongelar.
    """
    path = Path(path)
    if path.name == MARKER:
        return None
    current = path.parent if path.suffix or not path.is_dir() else path
    while True:
        if (current / MARKER).is_file():
            return current
        if root is not None and current.resolve() == root.resolve():
            return None
        if current.parent == current:
            return None
        current = current.parent


def staged_files(root):
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRD"],
        capture_output=True, text=True,
    )
    return [root / line for line in out.stdout.splitlines() if line.strip()]


def worktree_files(root):
    out = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMRD"],
        capture_output=True, text=True,
    )
    return [root / line for line in out.stdout.splitlines() if line.strip()]


def list_frozen(root):
    found = sorted(p.parent for p in root.rglob(MARKER)
                   if p.is_file() and ".git" not in p.parts)
    if not found:
        print("no hay directorios congelados")
        return 0
    print("directorios congelados:")
    for d in found:
        rel = d.relative_to(root)
        note = ""
        marker = d / MARKER
        first = marker.read_text(encoding="utf-8", errors="replace").strip().splitlines()
        if first:
            note = "  — " + first[0][:70]
        print("  {}{}".format(rel, note))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Verifica que no se toquen artefactos congelados.")
    ap.add_argument("paths", nargs="*", type=Path, help="rutas concretas a revisar")
    ap.add_argument("--worktree", action="store_true",
                    help="revisar tambien cambios sin agregar al indice")
    ap.add_argument("--list", action="store_true",
                    help="listar los directorios congelados")
    args = ap.parse_args()

    root = repo_root()
    if root is None:
        print("aviso: no es un repositorio git, no hay nada que revisar")
        return 0

    if args.list:
        return list_frozen(root)

    if args.paths:
        targets = [Path(p).resolve() for p in args.paths]
    else:
        targets = staged_files(root)
        if args.worktree:
            targets += worktree_files(root)

    violations = []
    for target in targets:
        frozen_dir = frozen_ancestor(target, root)
        if frozen_dir is not None:
            violations.append((target, frozen_dir))

    if not violations:
        return 0

    print()
    print("BLOQUEADO: se intento modificar un artefacto congelado.")
    print()
    seen = set()
    for target, frozen_dir in violations:
        try:
            t = target.relative_to(root)
            d = frozen_dir.relative_to(root)
        except ValueError:
            t, d = target, frozen_dir
        print("  {}".format(t))
        if str(d) not in seen:
            seen.add(str(d))
            print("      congelado por: {}/{}".format(d, MARKER))
    print()
    print("Un artefacto congelado es evidencia, no codigo de trabajo.")
    print("Si tiene un error, NO lo corrijas: crea una corrida nueva, anota en")
    print("docs/ que estaba mal en la anterior, y actualiza lo que dependia de ella.")
    print()
    print("Si de verdad hay que descongelarlo, borra el archivo {} a mano.".format(MARKER))
    print("Eso deja registro en git de quien lo descongelo y cuando.")
    print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
