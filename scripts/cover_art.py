from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from print_specs import (
    BLEED,
    SPINE_TEXT_MIN_PAGES,
    TRIM_6X9,
    full_wrap_size,
    spine_width,
)


@dataclass(frozen=True)
class CoverMetadata:
    title: str
    subtitle: str
    author: str
    back_blurb: str
    back_disclaimer: str


def build_ebook_cover(
    output: Path,
    metadata: CoverMetadata,
    theme_path: Path,
) -> None:
    theme = _load_theme(theme_path)
    palette = theme["palette"]
    front = theme["front"]
    width, height = int(front["width"]), int(front["height"])
    margin = int(front["margin"])

    image = _gradient(width, height, palette["background_top"], palette["background_bottom"])
    draw = ImageDraw.Draw(image)
    _draw_cover_texture(draw, (0, 0, width, height), palette, step=118)

    fonts = _front_fonts(theme)
    shadow = palette["shadow"]
    accent = palette["accent"]
    text = palette["text"]
    muted = palette["muted_text"]

    _draw_text(
        draw,
        (margin, 140),
        front["eyebrow"],
        fonts["eyebrow"],
        accent,
        shadow=shadow,
    )

    title_base = _remove_suffix(metadata.title, front["title_badge"])
    title_font, title_lines = _fit_wrapped_lines(
        title_base,
        theme,
        "bold",
        int(front["title_font_size"]),
        112,
        int(front["title_max_width"]),
        3,
    )
    y = 275
    for line in title_lines:
        _draw_text(draw, (margin, y), line, title_font, text, shadow=shadow)
        y += title_font.size + 22

    badge_y = y + 12
    badge_font = fonts["badge"]
    badge_text = front["title_badge"]
    badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_w = badge_bbox[2] - badge_bbox[0] + 56
    badge_h = badge_bbox[3] - badge_bbox[1] + 34
    draw.rounded_rectangle(
        [margin, badge_y, margin + badge_w, badge_y + badge_h],
        radius=18,
        fill=accent,
    )
    _draw_text(
        draw,
        (margin + 28, badge_y + 13),
        badge_text,
        badge_font,
        palette["background_top"],
    )
    y = badge_y + badge_h + 44
    draw.line([(margin, y), (margin + 620, y)], fill=accent, width=8)

    chart_bounds = (margin, 910, width - margin, 1665)
    _draw_chart(draw, chart_bounds, palette)

    subtitle_font = fonts["subtitle"]
    subtitle_y = 1785
    for line in _wrap_by_width(metadata.subtitle, subtitle_font, width - 2 * margin):
        _draw_text(draw, (margin, subtitle_y), line, subtitle_font, muted, shadow=shadow)
        subtitle_y += subtitle_font.size + 17

    _draw_text(
        draw,
        (margin, 2265),
        metadata.author,
        fonts["author"],
        text,
        shadow=shadow,
    )
    footer = "  |  ".join(front["footer_badges"])
    _draw_text(draw, (margin, 2334), footer, fonts["footer"], accent, shadow=shadow)

    image.save(output, "JPEG", quality=95, optimize=True)


def build_print_cover(
    output: Path,
    front_cover: Path,
    pages: int,
    paper: str,
    metadata: CoverMetadata,
    theme_path: Path,
) -> None:
    theme = _load_theme(theme_path)
    palette = theme["palette"]
    print_theme = theme["print"]

    spine = spine_width(pages, paper)
    wrap_w_in, wrap_h_in = full_wrap_size(*TRIM_6X9, spine)
    dpi = int(print_theme["dpi"])
    page_w, page_h = round(wrap_w_in * dpi), round(wrap_h_in * dpi)
    bleed_px = round(BLEED * dpi)
    trim_w_px = round(TRIM_6X9[0] * dpi)
    spine_px = round(spine * dpi)
    safe = round(float(print_theme["safe_margin_in"]) * dpi)

    back_x0 = bleed_px
    spine_x0 = back_x0 + trim_w_px
    front_x0 = spine_x0 + spine_px

    canvas = _gradient(
        page_w,
        page_h,
        palette["background_top"],
        palette["background_bottom"],
    )
    draw = ImageDraw.Draw(canvas)
    _draw_cover_texture(draw, (0, 0, spine_x0, page_h), palette, step=118)

    _paste_front_panel(canvas, front_cover, front_x0)
    draw = ImageDraw.Draw(canvas)

    draw.rectangle([spine_x0, 0, front_x0, page_h], fill=palette["spine"])
    if pages >= SPINE_TEXT_MIN_PAGES:
        _draw_spine_text(canvas, metadata, theme, (spine_x0, 0, front_x0, page_h))

    _draw_back_cover(
        draw,
        metadata,
        theme,
        (back_x0, bleed_px, spine_x0, page_h - bleed_px),
        safe,
        dpi,
    )

    canvas.save(output, "PDF", resolution=dpi)


def _load_theme(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _front_fonts(theme: dict) -> dict[str, ImageFont.FreeTypeFont]:
    front = theme["front"]
    return {
        "eyebrow": _font(theme, "bold", 38),
        "badge": _font(theme, "bold", 42),
        "subtitle": _font(theme, "regular", int(front["subtitle_font_size"])),
        "author": _font(theme, "bold", int(front["author_font_size"])),
        "footer": _font(theme, "regular", 34),
    }


def _font(theme: dict, kind: str, size: int) -> ImageFont.FreeTypeFont:
    configured = theme.get("fonts", {}).get(kind)
    fallbacks = [
        configured,
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if kind == "bold" else None,
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if kind == "bold" else None,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in fallbacks:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default(size=size)


def _gradient(width: int, height: int, top: str, bottom: str) -> Image.Image:
    image = Image.new("RGB", (width, height), top)
    draw = ImageDraw.Draw(image)
    top_rgb, bottom_rgb = _rgb(top), _rgb(bottom)
    for y in range(height):
        t = y / max(height - 1, 1)
        color = tuple(round(a + (b - a) * t) for a, b in zip(top_rgb, bottom_rgb))
        draw.line([(0, y), (width, y)], fill=color)
    return image


def _rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def _draw_cover_texture(
    draw: ImageDraw.ImageDraw,
    bounds: tuple[int, int, int, int],
    palette: dict,
    step: int,
) -> None:
    x0, y0, x1, y1 = bounds
    grid = palette["grid"]
    for x in range(x0 + step, x1, step):
        draw.line([(x, y0 + 270), (x, y1 - 260)], fill=grid, width=1)
    for y in range(y0 + 330, y1 - 280, step):
        draw.line([(x0 + 70, y), (x1 - 70, y)], fill=grid, width=1)
    for offset in range(-400, x1, 360):
        draw.line(
            [(offset, y1 - 110), (offset + 420, y1 - 530)],
            fill=palette["panel_border"],
            width=1,
        )


def _draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: str,
    shadow: str | None = None,
    anchor: str | None = None,
) -> None:
    kwargs = {"font": font, "fill": fill}
    if anchor:
        kwargs["anchor"] = anchor
    if shadow:
        sx, sy = xy[0] + 3, xy[1] + 4
        draw.text((sx, sy), text, font=font, fill=shadow, anchor=anchor)
    draw.text(xy, text, **kwargs)


def _remove_suffix(text: str, suffix: str) -> str:
    if text.lower().endswith(suffix.lower()):
        return text[: -len(suffix)].strip(" -:").strip()
    return text


def _fit_wrapped_lines(
    text: str,
    theme: dict,
    font_kind: str,
    start_size: int,
    min_size: int,
    max_width: int,
    max_lines: int,
) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(start_size, min_size - 1, -4):
        font = _font(theme, font_kind, size)
        lines = _wrap_by_width(text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines
    font = _font(theme, font_kind, min_size)
    return font, _wrap_by_width(text, font, max_width)


def _wrap_by_width(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        current = ""
        for word in paragraph.split():
            trial = f"{current} {word}".strip()
            if not current or font.getlength(trial) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def _draw_chart(
    draw: ImageDraw.ImageDraw,
    bounds: tuple[int, int, int, int],
    palette: dict,
) -> None:
    x0, y0, x1, y1 = bounds
    draw.rounded_rectangle(
        [x0, y0, x1, y1],
        radius=26,
        fill=palette["panel"],
        outline=palette["panel_border"],
        width=2,
    )
    for x in range(x0 + 115, x1, 115):
        draw.line([(x, y0 + 34), (x, y1 - 34)], fill=palette["grid"], width=1)
    for y in range(y0 + 95, y1, 95):
        draw.line([(x0 + 34, y), (x1 - 34, y)], fill=palette["grid"], width=1)

    candles = [
        (0.09, 0.68, 0.48, 0.83, 0.92, True),
        (0.18, 0.58, 0.40, 0.75, 0.86, True),
        (0.27, 0.64, 0.46, 0.79, 0.88, False),
        (0.36, 0.52, 0.34, 0.68, 0.81, True),
        (0.45, 0.43, 0.25, 0.60, 0.72, True),
        (0.54, 0.50, 0.32, 0.65, 0.78, False),
        (0.63, 0.34, 0.18, 0.54, 0.67, True),
        (0.72, 0.29, 0.13, 0.47, 0.59, True),
        (0.81, 0.38, 0.23, 0.57, 0.69, False),
        (0.90, 0.24, 0.08, 0.40, 0.52, True),
    ]
    chart_w, chart_h = x1 - x0, y1 - y0
    ma_points: list[tuple[int, int]] = []
    for cx_rel, top_rel, open_rel, close_rel, bottom_rel, up in candles:
        cx = round(x0 + cx_rel * chart_w)
        wick_top = round(y0 + top_rel * chart_h)
        open_y = round(y0 + open_rel * chart_h)
        close_y = round(y0 + close_rel * chart_h)
        wick_bottom = round(y0 + bottom_rel * chart_h)
        color = palette["positive"] if up else palette["negative"]
        body_top, body_bottom = sorted((open_y, close_y))
        draw.line([(cx + 4, wick_top + 6), (cx + 4, wick_bottom + 6)], fill=palette["shadow"], width=8)
        draw.rounded_rectangle(
            [cx - 30 + 4, body_top + 6, cx + 30 + 4, body_bottom + 6],
            radius=12,
            fill=palette["shadow"],
        )
        draw.line([(cx, wick_top), (cx, wick_bottom)], fill=color, width=8)
        draw.rounded_rectangle(
            [cx - 30, body_top, cx + 30, body_bottom],
            radius=12,
            fill=color,
        )
        ma_points.append((cx, round((open_y + close_y) / 2)))
    if len(ma_points) > 1:
        draw.line(ma_points, fill=palette["accent"], width=5, joint="curve")


def _paste_front_panel(canvas: Image.Image, cover: Path, front_x0: int) -> None:
    art = Image.open(cover).convert("RGB")
    front_w, front_h = canvas.width - front_x0, canvas.height
    scale = max(front_w / art.width, front_h / art.height)
    resized = art.resize(
        (round(art.width * scale), round(art.height * scale)),
        Image.LANCZOS,
    )
    left = (resized.width - front_w) // 2
    top = (resized.height - front_h) // 2
    canvas.paste(resized.crop((left, top, left + front_w, top + front_h)), (front_x0, 0))


def _draw_spine_text(
    canvas: Image.Image,
    metadata: CoverMetadata,
    theme: dict,
    bounds: tuple[int, int, int, int],
) -> None:
    x0, y0, x1, y1 = bounds
    width, height = max(x1 - x0, 1), y1 - y0
    font = _font(theme, "bold", min(28, max(width - 8, 10)))
    label = f"{metadata.title}  |  {metadata.author}"
    strip = Image.new("RGBA", (height, width), (0, 0, 0, 0))
    draw = ImageDraw.Draw(strip)
    draw.text((height // 2, width // 2), label, font=font, fill=theme["palette"]["text"], anchor="mm")
    rotated = strip.rotate(90, expand=True)
    canvas.paste(rotated.convert("RGB"), (x0, y0), rotated)


def _draw_back_cover(
    draw: ImageDraw.ImageDraw,
    metadata: CoverMetadata,
    theme: dict,
    bounds: tuple[int, int, int, int],
    safe: int,
    dpi: int,
) -> None:
    palette = theme["palette"]
    print_theme = theme["print"]
    x0, y0, x1, y1 = bounds
    left = x0 + safe
    right = x1 - safe
    max_width = right - left

    eyebrow_font = _font(theme, "bold", 30)
    title_font = _font(theme, "bold", 50)
    blurb_font = _font(theme, "regular", 29)
    small_font = _font(theme, "regular", 23)
    label_font = _font(theme, "bold", 24)
    shadow = palette["shadow"]

    y = y0 + safe
    _draw_text(draw, (left, y), print_theme["back_eyebrow"], eyebrow_font, palette["accent"], shadow=shadow)
    y += 58
    for line in _wrap_by_width(metadata.title, title_font, max_width):
        _draw_text(draw, (left, y), line, title_font, palette["text"], shadow=shadow)
        y += 58
    y += 24
    draw.line([(left, y), (left + min(500, max_width), y)], fill=palette["accent"], width=6)
    y += 50

    for line in _wrap_by_width(metadata.back_blurb, blurb_font, max_width):
        if line:
            _draw_text(draw, (left, y), line, blurb_font, palette["muted_text"], shadow=shadow)
        y += 39

    y += 30
    for line in _wrap_by_width(metadata.back_disclaimer, small_font, max_width):
        _draw_text(draw, (left, y), line, small_font, palette["quiet_text"], shadow=shadow)
        y += 31

    pill_text = "Spot Testnet"
    pill_bbox = draw.textbbox((0, 0), pill_text, font=label_font)
    pill_w = pill_bbox[2] - pill_bbox[0] + 42
    pill_h = pill_bbox[3] - pill_bbox[1] + 26
    pill_y = y1 - safe - round(float(print_theme["barcode_height_in"]) * dpi) - 58
    draw.rounded_rectangle(
        [left, pill_y, left + pill_w, pill_y + pill_h],
        radius=14,
        outline=palette["accent"],
        width=3,
    )
    _draw_text(draw, (left + 21, pill_y + 10), pill_text, label_font, palette["accent"])

    box_w = round(float(print_theme["barcode_width_in"]) * dpi)
    box_h = round(float(print_theme["barcode_height_in"]) * dpi)
    box_r, box_b = right, y1 - safe
    draw.rounded_rectangle(
        [box_r - box_w, box_b - box_h, box_r, box_b],
        radius=4,
        fill="#FFFFFF",
    )
    draw.text(
        (box_r - box_w + 18, box_b - box_h + 18),
        print_theme["barcode_label"],
        fill="#444444",
        font=small_font,
    )
