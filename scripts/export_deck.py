#!/usr/bin/env python3
"""Exporta un deck de Slidev a PDF u otro formato.

Envuelve la llamada a `npx @slidev/cli export` y facilita la instalacion de
las dependencias de Playwright necesarias para exportar a PDF.

Uso:
    python export_deck.py <destino>/slides.md [--format pdf|png|pptx|md] [--install-deps]
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# En Windows los lanzadores de Node son .cmd y CreateProcess no agrega la
# extension solo: sin resolver la ruta, subprocess falla con FileNotFoundError
# aunque Node este instalado.
NPX = shutil.which("npx.cmd") or shutil.which("npx") or "npx"
NPM = shutil.which("npm.cmd") or shutil.which("npm") or "npm"

# En Windows la consola suele venir en cp1252 y rompe los acentos.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def run_export(slides_path, fmt, timeout, output, dark, theme):
    cmd = [NPX, "@slidev/cli", "export", str(slides_path), "--format", fmt]
    if timeout:
        cmd.extend(["--timeout", str(timeout)])
    if output:
        cmd.extend(["--output", output])
    if dark:
        cmd.append("--dark")
    if theme:
        cmd.extend(["--theme", theme])

    try:
        print("Ejecutando: {}".format(" ".join(cmd)))
        result = subprocess.run(cmd)
        return result.returncode == 0
    except FileNotFoundError:
        print("\nERROR: npx no esta disponible. Hace falta instalar Node.js.", file=sys.stderr)
        return False


def install_playwright(workdir):
    # Sin cwd, npm instala en el directorio desde donde se invoca el script, no
    # en el del deck: en un proyecto sin package.json eso deja node_modules
    # tirado donde no corresponde y el export sigue fallando igual.
    print("Instalando dependencias de exportacion a PDF en {}...".format(workdir))
    try:
        subprocess.run([NPM, "i", "-D", "playwright-chromium"], check=True, cwd=str(workdir))
        subprocess.run([NPX, "playwright", "install", "chromium"], check=True, cwd=str(workdir))
        print("Dependencias instaladas correctamente.\n")
        return True
    except subprocess.CalledProcessError as e:
        print("\nERROR: fallo la instalacion de dependencias (codigo {}).".format(e.returncode), file=sys.stderr)
        return False
    except FileNotFoundError:
        print("\nERROR: npm no esta disponible. Hace falta instalar Node.js.", file=sys.stderr)
        return False


def main():
    ap = argparse.ArgumentParser(description="Exporta un deck de Slidev a PDF (o png/pptx/md).")
    ap.add_argument("slides", type=Path, help="ruta al archivo slides.md")
    ap.add_argument("--format", default="pdf", choices=["pdf", "png", "pptx", "md"], 
                    help="formato de salida (por defecto: pdf)")
    ap.add_argument("--timeout", type=int, 
                    help="timeout en ms para renderizar (ej. 60000)")
    ap.add_argument("--output", help="ruta de salida (opcional)")
    ap.add_argument("--dark", action="store_true", help="exportar usando el tema oscuro")
    ap.add_argument("--theme", help="sobrescribir el tema definido en el markdown (ej. seriph, apple-basic)")
    ap.add_argument("--install-deps", action="store_true", 
                    help="instala playwright-chromium y su navegador (requerido para PDF)")
    
    args = ap.parse_args()

    if not args.slides.exists():
        print("ERROR: no existe {}".format(args.slides), file=sys.stderr)
        return 2

    if args.install_deps:
        if not install_playwright(args.slides.resolve().parent):
            return 1

    success = run_export(args.slides, args.format, args.timeout, args.output, args.dark, args.theme)
    
    if not success and args.format == "pdf" and not args.install_deps:
        print("\nSi el export fallo porque 'Executable doesn't exist' o falta el navegador,", file=sys.stderr)
        print("corregilo corriendo el instalador de dependencias:", file=sys.stderr)
        print("    python {} {} --install-deps\n".format(sys.argv[0], args.slides), file=sys.stderr)
        return 1

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
