"""Radar-chart SVG generator.

Seam: `render(data, theme_name) -> str` is a pure function — given radar data and a
theme name it returns SVG markup, with no network or filesystem access. `main()` wraps
it with file I/O so the same renderer drives both the skill radar and the language radar.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from theme import theme as get_theme

# Geometry (viewBox units).
_W = 460
_H = 400
_CX = 230
_CY = 205
_R = 135
_RINGS = (0.25, 0.5, 0.75, 1.0)


def _validate(data: dict) -> list[dict]:
    if not isinstance(data, dict):
        raise ValueError("radar data must be an object")
    axes = data.get("axes")
    if not isinstance(axes, list) or len(axes) < 3:
        raise ValueError("radar data needs an 'axes' list with at least 3 entries")
    clean: list[dict] = []
    for i, ax in enumerate(axes):
        if not isinstance(ax, dict) or "label" not in ax or "value" not in ax:
            raise ValueError(f"axis {i} must have 'label' and 'value'")
        label = ax["label"]
        value = ax["value"]
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"axis {i} label must be a non-empty string")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"axis {i} value must be a number, got {value!r}")
        if not 0 <= value <= 100:
            raise ValueError(f"axis {i} value {value} out of range 0..100")
        clean.append({"label": label.strip(), "value": float(value)})
    return clean


def _point(cx: float, cy: float, radius: float, angle_deg: float) -> tuple[float, float]:
    a = math.radians(angle_deg)
    return (cx + radius * math.cos(a), cy + radius * math.sin(a))


def _fmt(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".")


def render(data: dict, theme_name: str) -> str:
    """Pure render seam: radar data + theme name -> SVG string."""
    axes = _validate(data)
    t = get_theme(theme_name)
    n = len(axes)
    title = escape(str(data.get("title", "")).strip())

    # Angles start at the top (-90deg) and go clockwise.
    angles = [-90 + i * 360 / n for i in range(n)]

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_W} {_H}" '
        f'width="{_W}" height="{_H}" role="img" '
        f'aria-label="{title or "radar chart"}" font-family="\'JetBrains Mono\',\'SFMono-Regular\',Consolas,monospace">'
    )
    parts.append(f'<rect width="{_W}" height="{_H}" rx="14" fill="{t["bg"]}"/>')
    if title:
        parts.append(
            f'<text x="{_CX}" y="34" text-anchor="middle" font-size="15" '
            f'font-weight="700" fill="{t["accent"]}" letter-spacing="1">{title}</text>'
        )

    # Concentric grid rings.
    for ring in _RINGS:
        pts = " ".join(
            f"{_fmt(x)},{_fmt(y)}"
            for x, y in (_point(_CX, _CY, _R * ring, a) for a in angles)
        )
        parts.append(
            f'<polygon points="{pts}" fill="none" stroke="{t["grid"]}" stroke-width="1"/>'
        )

    # Spokes + axis labels.
    for ax, a in zip(axes, angles):
        ex, ey = _point(_CX, _CY, _R, a)
        parts.append(
            f'<line x1="{_CX}" y1="{_CY}" x2="{_fmt(ex)}" y2="{_fmt(ey)}" '
            f'stroke="{t["grid"]}" stroke-width="1"/>'
        )
        lx, ly = _point(_CX, _CY, _R + 20, a)
        cos = math.cos(math.radians(a))
        anchor = "middle" if abs(cos) < 0.3 else ("start" if cos > 0 else "end")
        parts.append(
            f'<text x="{_fmt(lx)}" y="{_fmt(ly + 4)}" text-anchor="{anchor}" '
            f'font-size="11" fill="{t["muted"]}">{escape(ax["label"])}</text>'
        )

    # Data polygon.
    data_pts = [
        _point(_CX, _CY, _R * (ax["value"] / 100), a) for ax, a in zip(axes, angles)
    ]
    poly = " ".join(f"{_fmt(x)},{_fmt(y)}" for x, y in data_pts)
    parts.append(
        f'<polygon points="{poly}" fill="{t["accent_soft"]}" '
        f'stroke="{t["accent"]}" stroke-width="2" stroke-linejoin="round"/>'
    )
    for (x, y), ax in zip(data_pts, axes):
        parts.append(
            f'<circle cx="{_fmt(x)}" cy="{_fmt(y)}" r="3.2" fill="{t["accent"]}"/>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: radar.py <data.json> <out-prefix>", file=sys.stderr)
        return 2
    data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    prefix = argv[2]
    for th in ("dark", "light"):
        out = Path(f"{prefix}-{th}.svg")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(data, th) + "\n", encoding="utf-8")
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
