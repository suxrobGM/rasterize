# Font Loading

Fonts are bundled in `assets/fonts/` at the plugin root.

## Resolving the font directory

```python
import os
PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(PLUGIN_ROOT, "assets", "fonts")

# Or import the helper:
# from scripts.helpers import FONT_DIR, font_path, list_fonts
```

## Loading per engine

### Pillow

```python
from PIL import ImageFont

def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size * SCALE)

title_font = load_font("Outfit-Bold.ttf", 48)
```

### Cairo (native text — limited font selection)

```python
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(48)
```

For specific .ttf files, use Pango+PangoCairo (Linux only) or switch to
Playwright for text-heavy designs on Windows.

### Matplotlib

```python
from matplotlib import font_manager

for f in os.listdir(FONT_DIR):
    if f.endswith((".ttf", ".otf")):
        font_manager.fontManager.addfont(os.path.join(FONT_DIR, f))

plt.rcParams["font.family"] = "Outfit"
```

Register fonts BEFORE creating any figure.

### Plotly (system font stack)

Plotly renders via kaleido which uses system fonts. Copy bundled fonts
to the OS font directory — see `install_fonts_for_plotly()` in
`references/plotly.md`.

### Playwright (CSS @font-face)

```css
@font-face {
  font-family: 'Outfit';
  src: url('file:///absolute/path/to/assets/fonts/Outfit-Bold.ttf');
  font-weight: 700;
}
```

Use `file://` absolute paths. Wait for loading:

```python
page.evaluate("async () => { await document.fonts.ready; }")
page.wait_for_timeout(500)
```

## Font selection guide

| Style | Font files |
|-------|-----------|
| Headlines / bold display | BigShoulders-Bold, Outfit-Bold, YoungSerif |
| Body / clean sans | InstrumentSans, BricolageGrotesque, WorkSans |
| Serif / editorial | CrimsonPro, Lora, LibreBaskerville |
| Monospace / code / tech | JetBrainsMono, GeistMono, DMMono |
| Decorative / display | Boldonse, EricaOne, PoiretOne, NationalPark |
| Handwritten / casual | NothingYouCouldDo |

Max 2 font families per image. Always use absolute paths.
