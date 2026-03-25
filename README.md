# Rasterize

A Claude Code plugin for generating raster images (PNG, JPEG, WebP) from natural language prompts using Python rendering engines.

## Engines

| Engine | Best for |
| ------ | -------- |
| **Pillow** | Photo manipulation, compositing, filters, pixel ops |
| **Cairo** | Vector-style graphics, logos, icons, procedural art |
| **Matplotlib** | Statistical charts, scientific plots, data visualization |
| **Plotly** | Rich dashboards, annotated data viz, 3D surfaces |
| **Playwright** | HTML/CSS layouts, UI mockups, complex typography |

## Setup

```bash
# Install pdm if you don't have it
python -m pip install pdm --user

# Install all engines into a virtual environment
pdm install

# Install Playwright's Chromium browser
pdm run playwright install chromium
```

Or use the setup script:

```bash
python scripts/setup.py
```

## Usage

Install as a Claude Code plugin, then ask Claude to generate images:

- "Create a social media banner for my blog post"
- "Plot a bar chart showing quarterly revenue"
- "Design a minimalist logo for a company called Nexus"
- "Generate an Instagram story with bold typography"

Claude will pick the best engine, write a Python script, run it, and deliver the image.

## Project Structure

```text
rasterize/
  .claude-plugin/
    plugin.json             # Plugin manifest
  skills/image/
    SKILL.md                # Main skill definition
    shared/                 # Cross-engine patterns
      setup.md              # Installation & pdm setup
      fonts.md              # Font loading per engine
      canvas.md             # Dimensions, scaling, output formats
      themes.md             # Color palettes & themes
    references/             # Engine-specific reference docs
      pillow.md
      cairo.md
      matplotlib.md
      plotly.md
      playwright.md
  scripts/
    setup.py                # Cross-platform setup script
    check_engines.py        # Engine availability checker
    helpers.py              # Shared Python utilities
  assets/fonts/             # Bundled font files
  generated/                # Generated scripts & images (gitignored)
  pyproject.toml            # Dependencies (pdm)
```

## Checking Engine Status

```bash
pdm run python scripts/check_engines.py
```

## License

MIT
