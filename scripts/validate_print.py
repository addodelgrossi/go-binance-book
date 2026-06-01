"""Valida os artefatos de impressão do KDP (miolo 6x9 e capa wraparound).

Confere trim do miolo, contagem mínima de páginas e se as dimensões da capa
batem com a fórmula da lombada para a contagem real. Sai com status != 0 em
caso de falha (uso no `make validate`).
"""

from __future__ import annotations

import sys
from pathlib import Path

from pypdf import PdfReader

from print_specs import BLEED, MIN_PAGES, PAPER_THICKNESS, TRIM_6X9, full_wrap_size

ROOT = Path(__file__).resolve().parents[1]
PRINT_PDF = ROOT / "dist" / "robo-trade-go-binance-print-6x9.pdf"
PRINT_COVER = ROOT / "dist" / "robo-trade-go-binance-capa-print.pdf"
PAPER = "white"
TOL_IN = 0.02  # tolerância de arredondamento de pixel (≈ 6px a 300 DPI)


def _size_in(pdf: Path) -> tuple[float, float, int]:
    reader = PdfReader(str(pdf))
    box = reader.pages[0].mediabox
    return float(box.width) / 72, float(box.height) / 72, len(reader.pages)


def main() -> int:
    errors: list[str] = []

    miolo_w, miolo_h, pages = _size_in(PRINT_PDF)
    print(f"miolo: {miolo_w:.3f}x{miolo_h:.3f} in, {pages} páginas")
    if abs(miolo_w - TRIM_6X9[0]) > TOL_IN or abs(miolo_h - TRIM_6X9[1]) > TOL_IN:
        errors.append(f"trim do miolo != 6x9 (obtido {miolo_w:.3f}x{miolo_h:.3f})")
    if pages < MIN_PAGES:
        errors.append(f"miolo com {pages} páginas (< mínimo {MIN_PAGES})")

    spine = pages * PAPER_THICKNESS[PAPER]
    exp_w, exp_h = full_wrap_size(*TRIM_6X9, spine)
    cover_w, cover_h, cover_pages = _size_in(PRINT_COVER)
    print(f"lombada: {spine:.4f} in (papel {PAPER}, sangria {BLEED} in)")
    print(f"capa: {cover_w:.3f}x{cover_h:.3f} in (esperado {exp_w:.3f}x{exp_h:.3f})")
    if cover_pages != 1:
        errors.append(f"capa deve ter 1 página (tem {cover_pages})")
    if abs(cover_w - exp_w) > TOL_IN or abs(cover_h - exp_h) > TOL_IN:
        errors.append("dimensão da capa não bate com a fórmula da lombada")

    if errors:
        print("FALHA na validação de impressão:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("OK: artefatos de impressão conformes ao KDP")
    return 0


if __name__ == "__main__":
    sys.exit(main())
