# youtongzheng.github.io

Website of Youtong Zheng and the WEAVE Lab (Weaving Empirical and Virtual Evidence), Department of Earth and Atmospheric Sciences, University of Houston: https://youtongzheng.github.io

- `content/` — all text, as YAML (one file per section).
- `static/` — styles, script, and images.
- `build.py` — turns `content/` into the HTML pages in `docs/`.
- `docs/` — the generated site that GitHub Pages serves.

To update: edit a file in `content/`, run `python build.py`, then commit and push. `python build.py --serve` previews the site at http://localhost:8000. See `AGENTS.md`.
