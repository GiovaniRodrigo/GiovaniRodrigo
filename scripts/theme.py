"""Shared theme tokens for the generated profile SVG assets.

Neutral-dark base (GitHub `#0d1117`) with a tech-neon accent system. Each theme
("dark" | "light") resolves to a flat dict of tokens the renderers consume. Neon
accents are ordered by contrast on the neutral-dark ground, highest first, and are
mapped to project complexity elsewhere.
"""

from __future__ import annotations

# Neon accents, highest-contrast-on-dark first. See spec: cyan > green > amber > teal.
NEON = {
    "cyan": "#00E5FF",
    "green": "#39FF14",
    "amber": "#FFB000",
    "teal": "#2DD4BF",
}
NEON_ORDER = ["cyan", "green", "amber", "teal"]

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "panel": "#161b22",
        "grid": "#30363d",
        "text": "#c9d1d9",
        "muted": "#8b949e",
        # Neon reads bright on dark, use it straight.
        "accent": NEON["cyan"],
        "accent_soft": "#00e5ff33",
        "chrome_red": "#ff5f56",
        "chrome_yellow": "#ffbd2e",
        "chrome_green": "#27c93f",
    },
    "light": {
        "bg": "#ffffff",
        "panel": "#f6f8fa",
        "grid": "#d0d7de",
        "text": "#24292f",
        "muted": "#57606a",
        # Pure neon is invisible on white, drop to a deeper, still-vivid variant.
        "accent": "#0891b2",
        "accent_soft": "#0891b21f",
        "chrome_red": "#ff5f56",
        "chrome_yellow": "#ffbd2e",
        "chrome_green": "#27c93f",
    },
}


def theme(name: str) -> dict:
    if name not in THEMES:
        raise ValueError(f"unknown theme {name!r}; expected one of {sorted(THEMES)}")
    return THEMES[name]
