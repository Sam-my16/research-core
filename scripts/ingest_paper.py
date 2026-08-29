#!/usr/bin/env python3
"""Convierte un PDF a texto utilizable como fuente citable, y audita el resultado.

Por que dos extractores
-----------------------
Ninguno gana siempre. Medido sobre 11 papers de PolSAR:

    markitdown  recupera 86-104% del texto en PDFs digitales modernos
    pdftotext   recupera mucho mas en scans viejos con capa de texto OCR
                (Lee 1994: markitdown 2182 palabras, pdftotext 5486)

Por eso este script corre los dos y se queda con el mas largo. La conversion
mas corta no es "mas limpia": es una que perdio secciones enteras.

El modo de falla que importa
----------------------------
Un `.md` truncado NO da error. El agente lo lee, no encuentra la seccion de
limitaciones —porque el conversor se la comio— y concluye que el paper no
reporta fallas. La conclusion es falsa y las citas que la acompanan verifican
limpias, porque salieron de ese archivo. El verificador de citas no puede
detectarlo: comprueba las citas contra la fuente, no la fuente contra el PDF.

Ese hueco lo tapa `--check`, comparando cada `.md` contra su PDF.

Uso:
    python ingest_paper.py <archivo.pdf> [-o <dir>] [--force]
    python ingest_paper.py --check <dir-md> [--pdf-dir <dir>]

`pdftotext` viene con poppler (incluido en Git for Windows).
`markitdown` es opcional:  pip install markitdown[pdf]
"""

import argparse
import re
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

# Un paper de una columna ronda 500-800 palabras/pagina; uno de dos columnas,
# 700-1000. Por debajo de este piso el conversor perdio la mayor parte.
MIN_WORDS_PER_PAGE = 250

# Un PDF con menos de esto por pagina no tiene capa de texto real: lo que sale
# es el sello de la biblioteca o el numero de pagina. Hace falta OCR.
SCAN_WORDS_PER_PAGE = 20

# Cuanto del texto del PDF tiene que sobrevivir a la conversion.
MIN_RECOVERY = 0.75


def words(text):
    return len(text.split())


# --- extractores -------------------------------------------------------------

def pdftotext_extract(pdf_path):
    """Texto plano via poppler.

    Sin `-layout` a proposito. Con `-layout` poppler preserva la posicion
    horizontal, y en un paper a dos columnas lee las dos a la vez, linea por
    linea, intercalandolas:

        Commonly used deep learning algorithms include deep belief
        image (usually converted to dB scale), while neglecting phase

    Una cita copiada de ahi es una frase que no existe en el paper — y pasa
    el verificador, porque si esta en el archivo fuente. Sin `-layout`,
    poppler aplica su heuristica de orden de lectura y las columnas salen
    en el orden correcto.
    """
    if shutil.which("pdftotext") is None:
        return None
    try:
        result = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", str(pdf_path), "-"],
            capture_output=True, timeout=180,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8", errors="replace")


def markitdown_extract(pdf_path):
    """Markdown via markitdown. Conserva enfasis y encabezados."""
    if shutil.which("markitdown") is None:
        return None
    try:
        result = subprocess.run(
            ["markitdown", str(pdf_path)], capture_output=True, timeout=300,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8", errors="replace")


def page_count(pdf_path):
    if shutil.which("pdfinfo") is None:
        return None
    try:
        result = subprocess.run(
            ["pdfinfo", str(pdf_path)], capture_output=True, timeout=60,
        )
    except (subprocess.TimeoutExpired, OSError):
        return None
    m = re.search(r"^Pages:\s+(\d+)", result.stdout.decode("utf-8", "replace"), re.M)
    return int(m.group(1)) if m else None


# --- auditoria ---------------------------------------------------------------

def find_pdf(md_path, pdf_dir):
    """Ubica el PDF de un `.md`, tolerando el doble `.pdf.md`."""
    stem = md_path.name
    for suffix in (".pdf.md", ".md"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    candidate = Path(pdf_dir) / (stem + ".pdf")
    return candidate if candidate.exists() else None


def audit(md_path, pdf_dir):
    """Devuelve (estado, mensaje) comparando el `.md` contra su PDF.

    Estados: OK, ROTO, SCAN, PARCIAL, SIN-PDF.
    """
    if not md_path.exists():
        return "ROTO", "no existe"
    text = md_path.read_text(encoding="utf-8", errors="replace")
    size = md_path.stat().st_size
    md_words = words(text)

    if size == 0 or not text.strip():
        base = "0 bytes — la conversion fallo por completo"
    elif size < MIN_BYTES:
        base = "solo {} bytes — probablemente truncado".format(size)
    else:
        base = None

    pdf = find_pdf(md_path, pdf_dir) if pdf_dir else None
    if pdf is None:
        if base:
            return "ROTO", base
        return "SIN-PDF", "{} palabras (sin PDF para comparar)".format(md_words)

    pages = page_count(pdf)
    raw = pdftotext_extract(pdf)
    pdf_words = words(raw) if raw else 0

    # Un PDF sin capa de texto no se arregla cambiando de conversor.
    if pages and pdf_words / pages < SCAN_WORDS_PER_PAGE:
        return "SCAN", (
            "el PDF es una imagen escaneada ({} palabras en {} pags) — "
            "hace falta OCR".format(pdf_words, pages)
        )

    if base:
        return "ROTO", base

    recovery = md_words / pdf_words if pdf_words else 0
    wpp = md_words / pages if pages else None

    detail = "{} palabras".format(md_words)
    if pages:
        detail += " / {} pags = {:.0f} p/pag".format(pages, wpp)
    detail += " | recupera {:.0f}% del PDF".format(recovery * 100)

    if recovery < MIN_RECOVERY or (wpp is not None and wpp < MIN_WORDS_PER_PAGE):
        return "PARCIAL", detail + "  <-- faltan secciones"
    return "OK", detail


def cmd_check(directory, pdf_dir):
    files = sorted(Path(directory).glob("*.md"))
    if not files:
        print("no hay .md en {}".format(directory))
        return 1

    if pdf_dir is None:
        guess = Path(directory).parent
        if list(guess.glob("*.pdf")):
            pdf_dir = guess
            print("comparando contra los PDF de {}\n".format(pdf_dir))
        else:
            print("aviso: no se encontraron PDF para comparar; solo se revisa "
                  "el tamano de los .md\n")

    counts = {}
    for f in files:
        state, msg = audit(f, pdf_dir)
        counts[state] = counts.get(state, 0) + 1
        print("{:<8}{:<62.62} {}".format(state, f.name, msg))

    print()
    print(", ".join("{} {}".format(v, k) for k, v in sorted(counts.items())))

    if counts.get("SCAN"):
        print()
        print("SCAN    — PDF sin capa de texto. Ningun conversor lo va a leer.")
        print("          Corre OCR (ocrmypdf) o consegui otra copia del paper.")
    if counts.get("PARCIAL"):
        print()
        print("PARCIAL — el .md perdio parte del PDF. Reconvertilo con este")
        print("          script: prueba los dos extractores y se queda con el")
        print("          mas completo. Un deck hecho sobre un .md parcial")
        print("          concluye que el paper 'no reporta' lo que el conversor")
        print("          se comio, y sus citas verifican limpias igual.")

    bad = sum(v for k, v in counts.items() if k in ("ROTO", "SCAN", "PARCIAL"))
    return 1 if bad else 0


# --- conversion --------------------------------------------------------------

def cmd_convert(pdf, out_dir, force):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / (pdf.stem + ".md")

    if dest.exists() and not force:
        print("ya existe {} (usa --force para sobrescribir)".format(dest.name))
        return 0

    pages = page_count(pdf)
    candidates = []
    for name, fn in (("pdftotext", pdftotext_extract),
                     ("markitdown", markitdown_extract)):
        text = fn(pdf)
        if text and text.strip():
            candidates.append((words(text), name, text))
            print("  {:<12} {} palabras".format(name, words(text)))
        else:
            print("  {:<12} no disponible o sin salida".format(name))

    if not candidates:
        print("\nERROR: ningun extractor produjo texto.", file=sys.stderr)
        print("Instala poppler (pdftotext) o markitdown.", file=sys.stderr)
        return 2

    candidates.sort(reverse=True)
    best_words, best_name, best_text = candidates[0]

    if pages and best_words / pages < SCAN_WORDS_PER_PAGE:
        print("\nROTO: el PDF es una imagen escaneada ({} palabras en {} pags)."
              .format(best_words, pages))
        print("Ningun conversor lo va a leer. Corre OCR primero:")
        print("    ocrmypdf --skip-text \"{}\" salida.pdf".format(pdf.name))
        return 1

    dest.write_text(best_text, encoding="utf-8")
    tail = ", {:.0f} palabras/pagina)".format(best_words / pages) if pages else ")"
    print("\nOK -> {}  ({}, {} palabras{}".format(
        dest.name, best_name, best_words, tail))

    if len(candidates) > 1:
        loser_words, loser_name, _ = candidates[1]
        if loser_words and best_words / loser_words > 1.5:
            print("nota: {} habria perdido el {:.0f}% del texto".format(
                loser_name, 100 - loser_words * 100 / best_words))
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Convertir y auditar papers como fuente citable.")
    ap.add_argument("pdf", nargs="?", type=Path, help="PDF a convertir")
    ap.add_argument("-o", "--out-dir", default=".", help="directorio de salida")
    ap.add_argument("--force", action="store_true", help="sobrescribir si existe")
    ap.add_argument("--check", metavar="DIR", help="auditar los .md de DIR")
    ap.add_argument("--pdf-dir", metavar="DIR",
                    help="donde estan los PDF (por defecto, el padre de --check)")
    args = ap.parse_args()

    if args.check:
        return cmd_check(args.check, args.pdf_dir)
    if not args.pdf:
        ap.error("hace falta un PDF, o --check DIR")
    if not args.pdf.exists():
        print("ERROR: no existe {}".format(args.pdf), file=sys.stderr)
        return 2
    return cmd_convert(args.pdf, args.out_dir, args.force)


if __name__ == "__main__":
    sys.exit(main())
