# Changelog

## 1.0.0 (2026-03-24)

### Added

- Multi-engine raster image generation skill (Pillow, Cairo, Matplotlib, Plotly, Playwright)
- Engine routing table with decision hints for automatic engine selection
- Shared reference docs for setup, fonts, canvas/output, and themes
- Per-engine reference docs with patterns, helpers, and gotchas
- Bundled font collection (30+ families) in `assets/fonts/`
- Cross-platform setup script (`scripts/setup.py`)
- Engine availability checker (`scripts/check_engines.py`)
- Shared Python helpers: color utilities, WCAG contrast checking, layout helpers, size presets
- pdm-managed virtual environment (no global pip installs)
