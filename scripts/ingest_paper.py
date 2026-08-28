#!/usr/bin/env python3
"""Convierte un PDF a markdown con markitdown y verifica que el resultado sirva.

El paso de conversion es opcional dentro del pipeline: si ya tenes los `.md`
de tus papers, usalos directamente. Este script existe para dos cosas:

  1. normalizar el nombre de salida (evitar el doble `.pdf.md`)
  2. **detectar conversiones vacias o truncadas**, que es el modo de falla
     silencioso que arruina un deck: un `.md` de 0 bytes no da error, y el
     agente termina escribiendo el paper de memoria.

Uso:
    python ingest_paper.py <archivo.pdf> [-o <dir-salida>] [--force]
    python ingest_paper.py --check <dir>     # auditar conversiones existentes

Requiere `markitdown` solo para convertir:
    pip install markitdown[pdf]
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# En Windows la consola suele venir en cp1252 y rompe los acentos del reporte.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# Por debajo de esto, una conversion de paper esta rota o truncada.
MIN_BYTES = 2000


def out_name(pdf_path, out_dir):
    """Nombre de salida sin el doble `.pdf.md`."""
    return Path(out_dir) / (pdf_path.stem + ".md")


def check_one(md_path):
    """Devuelve (ok, mensaje) para un markdown ya convertido."""
    if not md_path.exists():
        return False, "no existe"
    size = md_path.stat().st_size
    if size == 0:
        return False, "0 bytes — la conversion fallo por completo"
    if size < MIN_BYTES:
        return False, "solo {} bytes — probablemente truncado".format(size)
    text = md_path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        return False, "sin contenido util"
    return True, "{} bytes, {} lineas".format(size, len(text.splitlines()))


def cmd_check(directory):
    files = sorted(Path(directory).glob("*.md"))
    if not files:
        print("no hay .md en {}".format(directory))
        return 1
    bad = 0
    for f in files:
        ok, msg = check_one(f)
        print("{} {:<70} {}".format("OK  " if ok else "ROTO", f.name[:70], msg))
        if not ok:
            bad += 1
    print()
    print("{} archivos, {} rotos".format(len(files), bad))
    if bad:
        print()
        print("Los archivos rotos NO pueden usarse como fuente de un deck.")
        print("Reconvertilos o conseguí un PDF con capa de texto.")
    return 1 if bad else 0


def cmd_convert(pdf, out_dir, force):
    if shutil.which("markitdown") is None:
        print("ERROR: markitdown no esta instalado.", file=sys.stderr)
        print("       pip install markitdown[pdf]", file=sys.stderr)
        return 2

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_name(pdf, out_dir)

    if dest.exists() and not force:
        print("ya existe {} (usa --force para sobrescribir)".format(dest.name))
        return 0

    print("convirtiendo {} ...".format(pdf.name))
    result = subprocess.run(
        ["markitdown", str(pdf)], capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        print("ERROR: markitdown fallo", file=sys.stderr)
        print(result.stderr[:2000], file=sys.stderr)
        return 1

    dest.write_text(result.stdout, encoding="utf-8")
    ok, msg = check_one(dest)
    print("{} -> {}  ({})".format("OK" if ok else "ROTO", dest.name, msg))
    if not ok:
        print()
        print("La conversion no sirve como fuente. Causa habitual: el PDF es una")
        print("imagen escaneada sin capa de texto. Hace falta OCR previo.")
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description="Convertir y auditar papers en markdown.")
    ap.add_argument("pdf", nargs="?", type=Path, help="PDF a convertir")
    ap.add_argument("-o", "--out-dir", default=".", help="directorio de salida")
    ap.add_argument("--force", action="store_true", help="sobrescribir si existe")
    ap.add_argument("--check", metavar="DIR",
                    help="auditar los .md ya convertidos en DIR")
    args = ap.parse_args()

    if args.check:
        return cmd_check(args.check)
    if not args.pdf:
        ap.error("hace falta un PDF, o --check DIR")
    if not args.pdf.exists():
        print("ERROR: no existe {}".format(args.pdf), file=sys.stderr)
        return 2
    return cmd_convert(args.pdf, args.out_dir, args.force)


if __name__ == "__main__":
    sys.exit(main())
