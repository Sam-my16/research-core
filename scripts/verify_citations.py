#!/usr/bin/env python3
"""Verifica que cada afirmacion de un deck este respaldada por una cita literal
de la fuente que declara.

Contrato (ver workflows/paper-slides.md):

  - El deck declara sus fuentes en el frontmatter, bajo `sources:`.
  - Cada afirmacion factual en el cuerpo de una diapositiva lleva una marca
    `[^N]`.
  - Las notas del presentador de esa misma diapositiva contienen una entrada
    por marca:

        [^1] fuente_id :: <cita textual exacta>
        [^2] fuente_id :: EQ
        [^3] fuente_id :: NOT-REPORTED

  - Las citas textuales se verifican como substring exacto del archivo fuente,
    tras normalizar espacios, enfasis markdown y comillas tipograficas.
  - `EQ` marca una ecuacion transcrita: NO se verifica automaticamente porque
    la conversion PDF->markdown rompe las formulas. Se lista en el reporte
    para chequeo humano contra el PDF.
  - `NOT-REPORTED` marca algo que el paper no reporta. Es una salida valida.

Uso:
    python verify_citations.py <slides.md> [--strict] [--quiet]

Sale con codigo 1 si hay errores (o si hay avisos y se paso --strict).
Sin dependencias externas: solo biblioteca estandar.
"""

import argparse
import difflib
import re
import sys
import unicodedata
from pathlib import Path

# En Windows la consola suele venir en cp1252 y rompe los acentos del reporte.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# --- normalizacion -----------------------------------------------------------

_PUNCT_MAP = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "–": "-", "—": "-", "−": "-", "‐": "-", "‑": "-",
    " ": " ", " ": " ", " ": " ", " ": " ",
    "​": "", "﻿": "",
}


def normalize(text):
    """Reduce el texto a una forma comparable.

    Colapsa espacios, quita enfasis markdown y unifica comillas y guiones.
    Es deliberadamente permisivo con el formato y estricto con las palabras:
    el objetivo es detectar invencion, no diferencias tipograficas.
    """
    text = unicodedata.normalize("NFKC", text)
    for src, dst in _PUNCT_MAP.items():
        text = text.replace(src, dst)
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


# --- parseo del deck ---------------------------------------------------------

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
SLIDE_SEP_RE = re.compile(r"^---\s*$", re.MULTILINE)
NOTES_RE = re.compile(r"<!--(.*?)-->", re.DOTALL)
REF_RE = re.compile(r"\[\^([0-9]+)\]")
ENTRY_RE = re.compile(r"^\s*\[\^([0-9]+)\]\s+(\S+)\s*::\s*(.+?)\s*$")

EQ_MARKER = "EQ"
NOT_REPORTED_MARKER = "NOT-REPORTED"


def parse_sources(frontmatter, deck_path):
    """Extrae el bloque `sources:` del frontmatter sin depender de PyYAML."""
    sources = {}
    in_block = False
    for line in frontmatter.splitlines():
        if re.match(r"^sources:\s*$", line):
            in_block = True
            continue
        if in_block:
            if not line.strip():
                continue
            if not line.startswith((" ", "\t")):
                break
            m = re.match(r"^\s+([A-Za-z0-9_.-]+)\s*:\s*(.+?)\s*$", line)
            if m:
                key = m.group(1)
                raw = m.group(2).strip().strip('"').strip("'")
                sources[key] = (deck_path.parent / raw).resolve()
    return sources


def split_slides(body):
    """Divide el cuerpo del deck en diapositivas por el separador de Slidev."""
    parts = SLIDE_SEP_RE.split(body)
    return [(i + 1, p) for i, p in enumerate(parts)]


def parse_entries(notes_text):
    """Lee las entradas `[^N] fuente :: contenido` de las notas."""
    entries = {}
    duplicates = []
    for line in notes_text.splitlines():
        m = ENTRY_RE.match(line)
        if not m:
            continue
        num = m.group(1)
        source_id = m.group(2)
        payload = m.group(3)
        if num in entries:
            duplicates.append(num)
        entries[num] = (source_id, payload)
    return entries, duplicates


# --- heuristica de afirmaciones sin respaldo ---------------------------------

BULLET_RE = re.compile(r"^\s*[-*+]\s+(.*\S)\s*$")
STRUCTURAL_RE = re.compile(
    r"^(agenda|indice|contenido|fuente|source|referencias?|references?)\b", re.I
)


def unsupported_bullets(body):
    """Vinetas que parecen afirmar algo pero no citan nada.

    Solo genera avisos: la heuristica no puede distinguir con certeza una
    afirmacion factual de una transicion narrativa.
    """
    out = []
    for line in body.splitlines():
        m = BULLET_RE.match(line)
        if not m:
            continue
        text = m.group(1)
        if "[^" in text or STRUCTURAL_RE.match(text.strip()):
            continue
        if len(normalize(text)) < 25:
            continue
        out.append(text)
    return out


# --- verificacion ------------------------------------------------------------

class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.verified = 0
        self.transcribed = []
        self.not_reported = []

    def error(self, slide, msg):
        self.errors.append((slide, msg))

    def warn(self, slide, msg):
        self.warnings.append((slide, msg))


def closest_span(needle, haystack, width=140):
    """Devuelve el fragmento de la fuente mas parecido a la cita fallida.

    Sirve para distinguir 'lo invento' de 'lo copio con una palabra cambiada'.
    """
    if not needle:
        return None
    matcher = difflib.SequenceMatcher(None, needle, haystack, autojunk=False)
    match = matcher.find_longest_match(0, len(needle), 0, len(haystack))
    if match.size < max(12, len(needle) // 4):
        return None
    start = max(0, match.b - 20)
    return haystack[start:start + width]


def verify(deck_path):
    report = Report()
    raw = deck_path.read_text(encoding="utf-8")

    fm_match = FRONTMATTER_RE.match(raw)
    if not fm_match:
        report.error(0, "el deck no tiene frontmatter YAML al inicio")
        return report
    sources = parse_sources(fm_match.group(1), deck_path)
    if not sources:
        report.error(0, "el frontmatter no declara ninguna fuente bajo `sources:`")
        return report

    # Carga y normaliza cada fuente una sola vez.
    loaded = {}
    for sid, path in sources.items():
        if not path.exists():
            report.error(0, "fuente '{}': no existe {}".format(sid, path))
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if not text.strip():
            report.error(0, "fuente '{}': el archivo esta vacio ({})".format(sid, path.name))
            continue
        loaded[sid] = normalize(text)

    body = raw[fm_match.end():]
    for slide_no, slide in split_slides(body):
        notes_blocks = NOTES_RE.findall(slide)
        notes_text = "\n".join(notes_blocks)
        visible = NOTES_RE.sub("", slide)

        refs = set(REF_RE.findall(visible))
        entries, duplicates = parse_entries(notes_text)

        for num in sorted(duplicates):
            report.error(slide_no, "[^{}] esta definida mas de una vez".format(num))

        for num in sorted(refs, key=int):
            if num not in entries:
                report.error(
                    slide_no,
                    "[^{}] se usa en la diapositiva pero no tiene entrada en las notas".format(num),
                )

        for num in sorted(set(entries) - refs, key=int):
            report.warn(
                slide_no, "[^{}] esta definida en las notas pero no se usa".format(num)
            )

        for num in sorted(refs & set(entries), key=int):
            source_id, payload = entries[num]
            if source_id not in sources:
                report.error(
                    slide_no,
                    "[^{}] cita la fuente '{}', no declarada en el frontmatter".format(num, source_id),
                )
                continue
            if source_id not in loaded:
                continue  # el error de carga ya se reporto

            if payload.strip() == EQ_MARKER:
                report.transcribed.append((slide_no, num, source_id))
                continue
            if payload.strip() == NOT_REPORTED_MARKER:
                report.not_reported.append((slide_no, num, source_id))
                continue

            needle = normalize(payload)
            if len(needle) < 15:
                report.warn(
                    slide_no,
                    '[^{}] la cita es muy corta para ser evidencia: "{}"'.format(num, payload),
                )
            if needle in loaded[source_id]:
                report.verified += 1
            else:
                hint = closest_span(needle, loaded[source_id])
                msg = (
                    "[^{}] cita NO encontrada literalmente en '{}':\n"
                    '        buscado: "{}"'.format(num, source_id, payload.strip()[:160])
                )
                if hint:
                    msg += '\n        lo mas parecido en la fuente: "...{}..."'.format(hint)
                else:
                    msg += "\n        no hay nada parecido en la fuente"
                report.error(slide_no, msg)

        for text in unsupported_bullets(visible):
            report.warn(slide_no, 'vineta sin cita: "{}"'.format(text[:110]))

    return report


def main():
    ap = argparse.ArgumentParser(
        description="Verifica las citas literales de un deck contra sus fuentes."
    )
    ap.add_argument("deck", type=Path, help="ruta a slides.md")
    ap.add_argument("--strict", action="store_true",
                    help="tratar los avisos como errores")
    ap.add_argument("--quiet", action="store_true",
                    help="solo imprimir el resumen final")
    args = ap.parse_args()

    if not args.deck.exists():
        print("ERROR: no existe {}".format(args.deck), file=sys.stderr)
        return 2

    report = verify(args.deck.resolve())

    if not args.quiet:
        for slide, msg in report.errors:
            print("[ERROR] diapositiva {}: {}".format(slide, msg))
        for slide, msg in report.warnings:
            print("[aviso] diapositiva {}: {}".format(slide, msg))
        if report.transcribed:
            print()
            print("ECUACIONES TRANSCRITAS - requieren chequeo humano contra el PDF:")
            for slide, num, sid in report.transcribed:
                print("  diapositiva {}, [^{}] ({})".format(slide, num, sid))
        if report.not_reported:
            print()
            print("MARCADO COMO NO REPORTADO POR EL PAPER:")
            for slide, num, sid in report.not_reported:
                print("  diapositiva {}, [^{}] ({})".format(slide, num, sid))

    print()
    print("citas verificadas literalmente : {}".format(report.verified))
    print("ecuaciones transcritas         : {}  (chequeo humano)".format(len(report.transcribed)))
    print("marcado como no reportado      : {}".format(len(report.not_reported)))
    print("errores                        : {}".format(len(report.errors)))
    print("avisos                         : {}".format(len(report.warnings)))

    failed = bool(report.errors) or (args.strict and bool(report.warnings))
    print()
    print("RESULTADO: " + ("FALLA" if failed else "OK"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
