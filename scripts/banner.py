"""Animated terminal banner generator (`profile.sh --live`).

Seam: `render(data, theme_name) -> str` is pure. The banner is a macOS-style terminal
window whose lines reveal one after another (SMIL `<animate>`), with a blinking block
cursor. SMIL animations render on GitHub READMEs when the SVG is served as an image.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from theme import theme as get_theme

_W = 900
_PAD = 26
_LINE_H = 30
_TOP = 66  # below the title bar


def _validate(data: dict) -> tuple[str, list[dict]]:
    if not isinstance(data, dict):
        raise ValueError("banner data must be an object")
    prompt = data.get("prompt", "$ ./profile.sh --live")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("banner 'prompt' must be a non-empty string")
    lines = data.get("lines")
    if not isinstance(lines, list) or not lines:
        raise ValueError("banner needs a non-empty 'lines' list")
    clean: list[dict] = []
    for i, ln in enumerate(lines):
        if not isinstance(ln, dict) or "key" not in ln or "value" not in ln:
            raise ValueError(f"line {i} must have 'key' and 'value'")
        if not isinstance(ln["key"], str) or not isinstance(ln["value"], str):
            raise ValueError(f"line {i} 'key'/'value' must be strings")
        clean.append({"key": ln["key"], "value": ln["value"]})
    return prompt.strip(), clean


def render(data: dict, theme_name: str) -> str:
    prompt, lines = _validate(data)
    t = get_theme(theme_name)
    height = _TOP + _LINE_H * (len(lines) + 1) + _PAD

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_W} {height}" '
        f'width="{_W}" height="{height}" role="img" aria-label="profile.sh --live" '
        f'font-family="\'JetBrains Mono\',\'SFMono-Regular\',Consolas,monospace">'
    )
    # Window.
    parts.append(
        f'<rect x="1" y="1" width="{_W - 2}" height="{height - 2}" rx="12" '
        f'fill="{t["panel"]}" stroke="{t["grid"]}" stroke-width="1"/>'
    )
    # Title bar dots.
    for i, col in enumerate((t["chrome_red"], t["chrome_yellow"], t["chrome_green"])):
        parts.append(f'<circle cx="{28 + i * 22}" cy="26" r="6.5" fill="{col}"/>')
    parts.append(
        f'<text x="{_W / 2}" y="30" text-anchor="middle" font-size="12" '
        f'fill="{t["muted"]}">profile.sh — zsh</text>'
    )

    # Prompt line (always visible).
    parts.append(
        f'<text x="{_PAD}" y="{_TOP}" font-size="16" fill="{t["accent"]}">'
        f'{escape(prompt)}</text>'
    )

    # Output lines revealed sequentially.
    per = 0.55  # seconds between line reveals
    for i, ln in enumerate(lines):
        y = _TOP + _LINE_H * (i + 1)
        begin = 0.4 + i * per
        parts.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.28s" '
            f'begin="{begin:.2f}s" fill="freeze"/>'
            f'<text x="{_PAD}" y="{y}" font-size="16">'
            f'<tspan x="{_PAD}" fill="{t["accent"]}">▸</tspan>'
            f'<tspan x="{_PAD + 22}" fill="{t["muted"]}">{escape(ln["key"])}</tspan>'
            f'<tspan x="{_PAD + 170}" fill="{t["text"]}">{escape(ln["value"])}</tspan>'
            f"</text></g>"
        )

    # Blinking block cursor on a final prompt line.
    cy = _TOP + _LINE_H * (len(lines) + 1)
    cursor_begin = 0.4 + len(lines) * per
    parts.append(
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" '
        f'dur="0.2s" begin="{cursor_begin:.2f}s" fill="freeze"/>'
        f'<text x="{_PAD}" y="{cy}" font-size="16" fill="{t["accent"]}">$ </text>'
        f'<rect x="{_PAD + 18}" y="{cy - 13}" width="10" height="17" fill="{t["accent"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0" dur="1s" '
        f'begin="{cursor_begin + 0.2:.2f}s" repeatCount="indefinite"/>'
        f"</rect></g>"
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: banner.py <data.json> <out-prefix>", file=sys.stderr)
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
