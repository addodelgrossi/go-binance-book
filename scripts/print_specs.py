"""Cálculos puros de especificações de impressão do KDP (paperback).

Sem efeitos colaterais: só matemática das dimensões usadas pelo gerador e
pela validação. Referências confirmadas nas specs atuais do KDP.
"""

from __future__ import annotations

# Espessura por página, em polegadas, por tipo de papel.
PAPER_THICKNESS = {
    "white": 0.002252,
    "cream": 0.0025,
    "color": 0.002347,
}

BLEED = 0.125  # polegadas, em cada borda da capa
TRIM_6X9 = (6.0, 9.0)  # polegadas (largura, altura)
MIN_PAGES = 24  # mínimo do KDP para paperback
SPINE_TEXT_MIN_PAGES = 80  # abaixo disso, manter lombada lisa


def spine_width(pages: int, paper: str = "white") -> float:
    """Largura da lombada em polegadas = páginas × espessura do papel."""
    if pages < MIN_PAGES:
        raise ValueError(f"paperback exige no mínimo {MIN_PAGES} páginas")
    try:
        return pages * PAPER_THICKNESS[paper]
    except KeyError:
        raise ValueError(f"papel inválido: {paper!r}") from None


def full_wrap_size(
    trim_w: float, trim_h: float, spine: float, bleed: float = BLEED
) -> tuple[float, float]:
    """Dimensões da capa wraparound em polegadas (largura, altura)."""
    width = trim_w * 2 + spine + bleed * 2
    height = trim_h + bleed * 2
    return (width, height)


def gutter_for(pages: int) -> float:
    """Margem interna mínima (gutter) em polegadas, por tier de páginas do KDP."""
    if pages <= 150:
        return 0.375
    if pages <= 300:
        return 0.5
    if pages <= 500:
        return 0.625
    if pages <= 700:
        return 0.75
    return 0.875
