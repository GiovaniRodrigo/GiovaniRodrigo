"""Language-mix bar generator.

Seam: `render(data, theme_name) -> str` is pure. Renders a horizontal stacked bar with a
legend from language weights (any positive numbers; normalised to proportions here). This
is committed so the profile never shows a broken image; the optional metrics workflow can
publish a richer `metrics.languages.svg` alongside it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from theme import theme as get_theme

# Recognisable per-language colours (GitHub linguist-ish), legible on both themes.
LANG_COLORS = {
    "Python": "#3572A5",
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "PHP": "#4F5D95",
    "Go": "#00ADD8",
    "Shell": "#89e051",
    "Vue": "#41b883",
    "C": "#555555",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
}
_FALLBACK = "#8b949e"

_W = 480
_H = 150
_BAR_X = 24
_BAR_Y = 60
_BAR_W = _W - 48
_BAR_H = 18


def _validate(data: dict) -> list[dict]:
    axes = data.get("axes") if isinstance(data, dict) else None
    if not isinstance(axes, list) or not axes:
        raise ValueError("language data needs a non-empty 'axes' list")
    clean: list[dict] = []
    for i, ax in enumerate(axes):
        if not isinstance(ax, dict) or "label" not in ax or "value" not in ax:
            raise ValueError(f"entry {i} must have 'label' and 'value'")
        v = ax["value"]
        if isinstance(v, bool) or not isinstance(v, (int, float)) or v < 0:
            raise ValueError(f"entry {i} value must be a non-negative number")
        clean.append({"label": str(ax["label"]).strip(), "value": float(v)})
    if sum(a["value"] for a in clean) <= 0:
        raise ValueError("language values sum to zero")
    return clean


def render(data: dict, theme_name: str) -> str:
    axes = _validate(data)
    t = get_theme(theme_name)
    total = sum(a["value"] for a in axes)

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_W} {_H}" '
        f'width="{_W}" height="{_H}" role="img" aria-label="most used languages" '
        f'font-family="\'JetBrains Mono\',\'SFMono-Regular\',Consolas,monospace">'
    )
    parts.append(
        f'<rect x="1" y="1" width="{_W - 2}" height="{_H - 2}" rx="14" '
        f'fill="{t["panel"]}" stroke="{t["grid"]}" stroke-width="1"/>'
    )
    parts.append(
        f'<text x="24" y="38" font-size="15" font-weight="700" fill="{t["accent"]}">'
        f'most used languages</text>'
    )

    # Stacked bar.
    parts.append(
        f'<clipPath id="barclip"><rect x="{_BAR_X}" y="{_BAR_Y}" width="{_BAR_W}" '
        f'height="{_BAR_H}" rx="{_BAR_H / 2}"/></clipPath>'
    )
    parts.append(f'<g clip-path="url(#barclip)">')
    x = _BAR_X
    for a in axes:
        w = _BAR_W * a["value"] / total
        col = LANG_COLORS.get(a["label"], _FALLBACK)
        parts.append(f'<rect x="{x:.2f}" y="{_BAR_Y}" width="{w + 0.6:.2f}" height="{_BAR_H}" fill="{col}"/>')
        x += w
    parts.append("</g>")

    # Legend (two rows of three).
    lx0, ly0 = 24, 108
    for i, a in enumerate(axes):
        col = LANG_COLORS.get(a["label"], _FALLBACK)
        row, coln = divmod(i, 3)
        lx = lx0 + coln * 150
        ly = ly0 + row * 26
        pct = 100 * a["value"] / total
        parts.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="5.5" fill="{col}"/>')
        parts.append(
            f'<text x="{lx + 17}" y="{ly}" font-size="12" fill="{t["text"]}">'
            f'{escape(a["label"])} <tspan fill="{t["muted"]}">{pct:.0f}%</tspan></text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: langbar.py <data.json> <out-prefix>", file=sys.stderr)
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
