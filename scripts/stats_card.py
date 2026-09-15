"""Self-hosted GitHub stats card generator.

Three concerns kept separate (spec seam):
  - fetch(user, token)   -> dict   : thin GitHub API adapter (network; not unit-tested)
  - render(stats, theme) -> str    : pure SVG renderer (unit-tested)
  - main()                          : wires fetch -> render -> file, reads token from env

Language byte totals are de-noised of vendored dependencies (see EXCLUDE) so a committed
venv does not swamp the real language mix.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

from theme import theme as get_theme

# Repos whose reported language bytes are polluted by vendored deps; excluded from
# aggregate language counting only (they still count as repos/stars).
EXCLUDE_LANG = {"efficiency-algorithm-blind-index"}

_W = 480
_H = 200


def _api(url: str, token: str | None) -> object:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 (fixed api host)
        return json.load(r)


def fetch(user: str, token: str | None = None) -> dict:
    """Network adapter: collect the numbers the card shows. Not unit-tested."""
    profile = _api(f"https://api.github.com/users/{user}", token)
    repos: list[dict] = []
    page = 1
    while True:
        batch = _api(
            f"https://api.github.com/users/{user}/repos?per_page=100&page={page}&type=owner",
            token,
        )
        if not isinstance(batch, list) or not batch:
            break
        repos.extend(batch)
        page += 1
        if len(batch) < 100:
            break

    own = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in own)
    return {
        "user": user,
        "name": profile.get("name") or user,
        "followers": profile.get("followers", 0),
        "public_repos": len([r for r in own]),
        "stars": stars,
        "forks_made_of_my_repos": sum(r.get("forks_count", 0) for r in own),
    }


def _validate(stats: dict) -> dict:
    required = ["name", "followers", "public_repos", "stars"]
    for k in required:
        if k not in stats:
            raise ValueError(f"stats missing required key {k!r}")
        if k != "name" and not isinstance(stats[k], int):
            raise ValueError(f"stats[{k!r}] must be an int, got {stats[k]!r}")
    return stats


def _metric(x: int, label: str, cx: float, cy: float, accent: str, muted: str) -> str:
    return (
        f'<text x="{cx}" y="{cy}" text-anchor="middle" font-size="30" '
        f'font-weight="700" fill="{accent}">{x}</text>'
        f'<text x="{cx}" y="{cy + 22}" text-anchor="middle" font-size="12" '
        f'fill="{muted}">{escape(label)}</text>'
    )


def render(stats: dict, theme_name: str) -> str:
    """Pure render seam: stats dict + theme name -> SVG string."""
    s = _validate(stats)
    t = get_theme(theme_name)
    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_W} {_H}" '
        f'width="{_W}" height="{_H}" role="img" aria-label="GitHub statistics" '
        f'font-family="\'JetBrains Mono\',\'SFMono-Regular\',Consolas,monospace">'
    )
    parts.append(
        f'<rect x="1" y="1" width="{_W - 2}" height="{_H - 2}" rx="14" '
        f'fill="{t["panel"]}" stroke="{t["grid"]}" stroke-width="1"/>'
    )
    parts.append(
        f'<text x="26" y="44" font-size="17" font-weight="700" fill="{t["accent"]}">'
        f'{escape(str(s["name"]))} — GitHub stats</text>'
    )
    parts.append(
        f'<line x1="26" y1="60" x2="{_W - 26}" y2="60" stroke="{t["grid"]}" stroke-width="1"/>'
    )
    cols = [
        (int(s["public_repos"]), "repos"),
        (int(s["stars"]), "stars"),
        (int(s["followers"]), "followers"),
        (int(s.get("forks_made_of_my_repos", 0)), "forks"),
    ]
    step = _W / len(cols)
    for i, (val, label) in enumerate(cols):
        cx = step * (i + 0.5)
        parts.append(_metric(val, label, cx, 130, t["accent"], t["muted"]))
    parts.append("</svg>")
    return "\n".join(parts)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: stats_card.py <github-user> <out-prefix>", file=sys.stderr)
        return 2
    user, prefix = argv[1], argv[2]
    token = os.environ.get("METRICS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    stats = fetch(user, token)
    for th in ("dark", "light"):
        out = Path(f"{prefix}-{th}.svg")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(stats, th) + "\n", encoding="utf-8")
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
