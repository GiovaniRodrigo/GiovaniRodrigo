"""Regenerate every committed profile SVG asset.

Run from the repo root: `python scripts/generate.py`. The stats card needs no token for
public data, but a `METRICS_TOKEN`/`GITHUB_TOKEN` in the environment avoids API rate limits.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import banner  # noqa: E402
import langbar  # noqa: E402
import radar  # noqa: E402
import stats_card  # noqa: E402

USER = "GiovaniRodrigo"
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"


def main() -> int:
    banner.main(["banner.py", str(ASSETS / "banner.json"), str(ASSETS / "banner")])
    radar.main(["radar.py", str(ASSETS / "skills.json"), str(ASSETS / "radar")])
    radar.main(["radar.py", str(ASSETS / "langmix.json"), str(ASSETS / "radar-langs")])
    langbar.main(["langbar.py", str(ASSETS / "langmix.json"), str(ASSETS / "languages")])
    try:
        stats_card.main(["stats_card.py", USER, str(ASSETS / "card-stats")])
    except Exception as e:  # network failures shouldn't wipe the other assets
        print(f"WARN: stats card skipped ({e})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
