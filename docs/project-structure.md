# Project Structure

```text
rasterize/
  .claude-plugin/
    plugin.json               # Plugin manifest
  skills/render/
    SKILL.md                   # Skill definition and routing table
    shared/                    # Cross-engine patterns
      setup.md                 # Installation and pdm setup
      fonts.md                 # Font loading per engine
      canvas.md                # Dimensions, scaling, output formats
      themes.md                # Color palettes and themes
    references/                # Engine-specific reference docs
      pillow.md
      cairo.md
      matplotlib.md
      plotly.md
      playwright.md
  scripts/
    setup.py                   # Cross-platform setup script
    check_engines.py           # Engine availability checker
    helpers.py                 # Shared Python utilities
  assets/fonts/                # Bundled font files (30+ families)
  generated/                   # Generated scripts and images (gitignored)
  docs/                        # Documentation and example images
  pyproject.toml               # Dependencies (pdm)
```

## Key Directories

### `skills/render/`

The main skill definition. `SKILL.md` contains the routing table, design
principles, and script template that Claude follows when generating images.

### `skills/render/shared/`

Cross-engine reference docs for patterns shared across all engines:
setup, fonts, canvas/output, and color themes.

### `skills/render/references/`

Engine-specific reference docs with code patterns, helpers, and gotchas.
Claude reads the relevant file before writing a generation script.

### `scripts/`

Plugin utilities — setup, engine checker, and shared Python helpers
(color utilities, WCAG contrast, layout functions, size presets).

### `assets/fonts/`

30+ bundled font families (TTF) covering headlines, body, serif, mono,
decorative, and handwritten styles.

### `generated/`

Workspace for generated scripts and output images. Gitignored.
Scripts are kept after delivery for iteration; intermediate files
prefixed with `_tmp_` are cleaned up.

## Engine Status

Check which engines are installed:

```bash
pdm run python scripts/check_engines.py
```

Install any missing engines:

```bash
pdm run python scripts/check_engines.py --install
```
