---
name: render
description: >
  Generate raster images (PNG, JPEG, WebP) from natural language prompts using Python rendering engines. Covers graphics, charts, layouts, and procedural art. Not for SVG output.
---

# Rasterize — Multi-Engine Raster Image Generation

Generate professional raster images by routing each request to the best
rendering engine. You write Python code; the engine does the pixel work.

## Quick Start

1. Read the user's request
2. Pick an engine using the routing table below
3. Read the engine's reference doc from `./references/`
4. Write a self-contained Python script that outputs to the target path
5. Run the script using `pdm run python <script.py>` (to use the plugin's venv), verify the output, deliver the image

> **Environment**: This plugin uses a pdm-managed virtual environment.
> Always run generation scripts with `pdm run python` from the plugin root.
> If pdm is not set up yet, run `python scripts/setup.py` first.

## Engine Routing Table

| Request type | Engine | Reference file |
|---|---|---|
| Photo manipulation, compositing, filters, pixel ops, simple graphics | **Pillow** | `./references/pillow.md` |
| Clean vector-style graphics, logos, icons, anti-aliased shapes, typography-heavy designs | **Cairo** | `./references/cairo.md` |
| Statistical charts, scientific plots, data visualization (static) | **Matplotlib + Seaborn** | `./references/matplotlib.md` |
| Complex interactive-looking dashboards, rich data viz with annotations | **Plotly** (static export) | `./references/plotly.md` |
| Complex layouts, HTML/CSS designs, UI mockups, anything with web fonts or CSS effects | **Playwright** (HTML→PNG) | `./references/playwright.md` |

### Routing decision hints

- If the request mentions "chart", "plot", "graph", "histogram", "scatter",
  "heatmap", or data columns → **Matplotlib/Seaborn** (or **Plotly** for
  fancier output)
- If the request is about a logo, icon, badge, geometric design, or
  anything that needs crisp anti-aliased curves → **Cairo**
- If the request says "banner", "social media post", "thumbnail" with
  text overlays on photos → **Pillow**
- If the request describes a full-page layout, poster with complex
  typography, card design, or UI mockup → **Playwright**
- If the request is about generative/procedural/algorithmic art → **Cairo**
  (or **Pillow** if it's pixel-manipulation art like fractals)
- When in doubt between Pillow and Cairo → prefer **Cairo** (better quality)
- When in doubt between Matplotlib and Plotly → prefer **Matplotlib**
  (simpler, faster)

### Multi-engine compositions

Some requests need two engines. Common combos:

- **Matplotlib → Pillow**: Generate a chart, then composite it onto a
  branded background with logos and text overlays
- **Cairo → Pillow**: Draw clean vector shapes, then apply raster effects
  (blur, noise, texture)
- **Playwright → Pillow**: Render an HTML layout, then crop/resize/optimize

When combining engines, save intermediate outputs as temporary PNGs and
load them in the second engine.

## Shared References

These files contain cross-engine patterns — read them before the engine docs:

- `./shared/setup.md` — Installation, pdm setup, running scripts
- `./shared/fonts.md` — Font directory resolution, per-engine loading, font selection guide
- `./shared/canvas.md` — Dimensions, size presets, retina scaling, output saving (PNG/JPEG/WebP)
- `./shared/themes.md` — Dark/light themes, color tokens, categorical/sequential/diverging palettes

## Workspace

All generated files go into the `generated/` directory at the plugin root:

```
generated/
  <slug>_render.py      # generation script
  <slug>.png            # output image
```

- **Scripts**: Save as `generated/<slug>_render.py` where `<slug>` is a
  short kebab-case name derived from the request (e.g., `social-card_render.py`)
- **Output images**: Save as `generated/<slug>.png` (or `.jpg`/`.webp`)
- **Intermediates**: Save temporary files in `generated/` too — prefix with `_tmp_`
- The `generated/` directory is gitignored. Do NOT place scripts in `scripts/`
  or output in `output/` — those are not for generated artifacts.
- After delivering the final image, clean up intermediate `_tmp_*` files.
- **Keep the generation script** after completion — the user may want to
  iterate ("make the text bigger", "change the color") and the script
  enables re-rendering without rewriting from scratch.
- If the user explicitly asks to clean up, delete both the script and output.

## Script Structure

Every generation script should follow this pattern:

```python
#!/usr/bin/env python3
"""Rasterize: [brief description of what this generates]"""

import os

# === CONFIGURATION ===
WIDTH, HEIGHT = 1200, 630       # Logical dimensions
SCALE = 2                       # Retina multiplier

# Paths — all generated files go in generated/
PLUGIN_ROOT = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.join(PLUGIN_ROOT, "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(GENERATED_DIR, "<slug>.png")
FONT_DIR = os.path.join(PLUGIN_ROOT, "assets", "fonts")

# Engine-specific imports here

# === HELPERS ===
# Reusable drawing functions here

# === COMPOSITION ===
def render():
    # Main rendering logic
    # ...
    pass

# === EXECUTE ===
if __name__ == "__main__":
    render()
    print(f"Saved to {OUTPUT_PATH}")
```

## Design Principles

When generating images, aim for professional quality:

- **Whitespace**: Leave generous margins (at least 5-8% of canvas size).
  Content should breathe.
- **Color**: Use cohesive palettes. When the user doesn't specify colors,
  choose a palette with 1 primary, 1 accent, 1-2 neutrals. Avoid pure
  black (#000); use near-black (#1a1a2e or #0f172a) instead. Avoid pure
  white (#fff) on large areas; use off-white (#fafafa, #f8fafc).
- **Typography**: Maximum 2 font families per image. Establish clear
  hierarchy (title → subtitle → body → caption) through size and weight.
- **Alignment**: Use a grid. Align elements to consistent baselines and
  gutters. Misalignment is the #1 tell of AI-generated graphics.
- **Contrast**: Ensure text passes WCAG AA (4.5:1 ratio). Use a contrast
  checker function if needed.

## Error Handling

- If a required engine is not installed, follow `./shared/setup.md`.
- If a font file is missing, fall back to a safe default from the
  bundled collection (see `./shared/fonts.md`). Never use system fonts
  without checking availability.
- If rendering fails, check the error, fix the script, and retry.
  Common issues: missing font path, wrong image mode, Cairo surface not
  flushed before save.

## Engine Reference Docs

Before writing a generation script, ALWAYS read the relevant engine
reference doc from `./references/`. These contain engine-specific
patterns, gotchas, and helper snippets that prevent common mistakes.

- `./references/pillow.md` — Pillow patterns and helpers
- `./references/cairo.md` — PyCairo patterns and helpers
- `./references/matplotlib.md` — Matplotlib + Seaborn patterns
- `./references/plotly.md` — Plotly static export patterns
- `./references/playwright.md` — HTML-to-PNG via Playwright
