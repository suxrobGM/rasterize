# Cairo Engine Reference

Best for: clean vector-style graphics rendered to raster, logos, icons,
badges, geometric designs, typography-heavy designs, procedural art,
anything needing crisp anti-aliased curves and professional text rendering.

> **Setup**: See `shared/setup.md` | **Fonts**: See `shared/fonts.md`
> **Canvas & output**: See `shared/canvas.md` | **Themes**: See `shared/themes.md`

Additional Cairo install notes:

```bash
# On Windows, if pycairo fails: pip install pipwin && pipwin install pycairo
# On Linux: sudo apt-get install libcairo2-dev pkg-config python3-dev
```

## Core Patterns

### Basic canvas setup

```python
import cairo
import math

# See shared/canvas.md for dimension presets
WIDTH, HEIGHT = 1200, 630
SCALE = 2
W, H = WIDTH * SCALE, HEIGHT * SCALE

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(surface)
ctx.scale(SCALE, SCALE)  # Work in logical coordinates after this

# Background — see shared/themes.md for color tokens
ctx.set_source_rgba(0.06, 0.09, 0.16, 1)  # #0f172a
ctx.rectangle(0, 0, WIDTH, HEIGHT)
ctx.fill()
```

### Pango for advanced typography (recommended for text-heavy work)

```bash
# If pdm is not installed: python -m pip install pdm --user
pdm run pip install PyGObject
# Requires system packages (Linux only):
#   sudo apt-get install libgirepository1.0-dev gir1.2-pango-1.0
# Note: PyGObject/Pango is Linux-only. On Windows, use Cairo's
# built-in text rendering or switch to Playwright for text-heavy designs.
```

```python
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo

def draw_text(ctx, text, font_desc_str, x, y, color=(1,1,1), max_width=None):
    """Draw text using Pango for proper font rendering."""
    ctx.save()
    ctx.move_to(x, y)
    ctx.set_source_rgba(*color)

    layout = PangoCairo.create_layout(ctx)
    layout.set_text(text, -1)
    font_desc = Pango.FontDescription.from_string(font_desc_str)
    layout.set_font_description(font_desc)

    if max_width:
        layout.set_width(int(max_width * Pango.SCALE))
        layout.set_wrap(Pango.WrapMode.WORD_CHAR)

    PangoCairo.show_layout(ctx, layout)
    ctx.restore()

    # Return size for positioning
    ink, logical = layout.get_pixel_extents()
    return logical.width, logical.height
```

### Fallback: Cairo-native text (no Pango dependency)

```python
def draw_simple_text(ctx, text, size, x, y, color=(1,1,1,1),
                     font_face="sans-serif", weight=cairo.FONT_WEIGHT_NORMAL):
    ctx.save()
    ctx.select_font_face(font_face, cairo.FONT_SLANT_NORMAL, weight)
    ctx.set_font_size(size)
    ctx.set_source_rgba(*color)
    ctx.move_to(x, y)
    ctx.show_text(text)
    ctx.restore()

def measure_text(ctx, text, size, font_face="sans-serif"):
    ctx.save()
    ctx.select_font_face(font_face, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    extents = ctx.text_extents(text)
    ctx.restore()
    return extents.width, extents.height
```

### Shapes with anti-aliasing (native!)

Cairo anti-aliases everything by default.

```python
# Rounded rectangle
def rounded_rect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi/2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi/2)
    ctx.arc(x + r, y + h - r, r, math.pi/2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3*math.pi/2)
    ctx.close_path()

# Circle
def circle(ctx, cx, cy, radius):
    ctx.arc(cx, cy, radius, 0, 2 * math.pi)

# Usage
rounded_rect(ctx, 50, 50, 400, 200, 16)
ctx.set_source_rgba(0.23, 0.51, 0.96, 1)  # blue
ctx.fill_preserve()
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(1)
ctx.stroke()
```

### Linear gradient

```python
def linear_gradient(ctx, x0, y0, x1, y1, stops):
    """stops = [(offset, r, g, b, a), ...]"""
    pat = cairo.LinearGradient(x0, y0, x1, y1)
    for offset, r, g, b, a in stops:
        pat.add_color_stop_rgba(offset, r, g, b, a)
    ctx.set_source(pat)

# Usage
linear_gradient(ctx, 0, 0, WIDTH, HEIGHT, [
    (0.0, 0.06, 0.09, 0.16, 1.0),
    (1.0, 0.12, 0.10, 0.26, 1.0),
])
ctx.rectangle(0, 0, WIDTH, HEIGHT)
ctx.fill()
```

### Radial gradient

```python
pat = cairo.RadialGradient(cx, cy, inner_radius, cx, cy, outer_radius)
pat.add_color_stop_rgba(0, 0.23, 0.51, 0.96, 0.3)
pat.add_color_stop_rgba(1, 0.23, 0.51, 0.96, 0.0)
ctx.set_source(pat)
ctx.arc(cx, cy, outer_radius, 0, 2*math.pi)
ctx.fill()
```

### Drop shadow (manual)

```python
def with_shadow(ctx, draw_fn, offset=(4, 4), blur_steps=10, shadow_alpha=0.3):
    """Draw a shape with a soft shadow. draw_fn(ctx) draws the path."""
    # Shadow (multiple semi-transparent passes for blur approximation)
    for i in range(blur_steps):
        alpha = shadow_alpha * (1 - i / blur_steps) / blur_steps
        ctx.save()
        ctx.translate(offset[0], offset[1])
        draw_fn(ctx)
        ctx.set_source_rgba(0, 0, 0, alpha)
        ctx.fill()
        ctx.restore()

    # Actual shape
    draw_fn(ctx)
```

### Bezier curves

```python
ctx.move_to(100, 300)
ctx.curve_to(150, 100, 350, 500, 400, 300)  # control1, control2, end
ctx.set_source_rgba(0.23, 0.51, 0.96, 1)
ctx.set_line_width(3)
ctx.stroke()
```

### Clipping masks

```python
# Clip to a circle
ctx.arc(cx, cy, radius, 0, 2*math.pi)
ctx.clip()
# Everything drawn after this is clipped to the circle
# ...
ctx.reset_clip()
```

### Loading and drawing images

```python
# Load a PNG as a Cairo surface
image_surface = cairo.ImageSurface.create_from_png("input.png")

# Draw it at position, optionally scaled
ctx.save()
ctx.translate(x, y)
img_w = image_surface.get_width()
img_h = image_surface.get_height()
ctx.scale(target_w / img_w, target_h / img_h)
ctx.set_source_surface(image_surface, 0, 0)
ctx.paint()
ctx.restore()
```

## Common Gotchas

1. **Coordinate system** — Cairo's Y axis goes downward (same as screen).
   `ctx.scale(SCALE, SCALE)` should be called early so you work in logical
   coordinates.
2. **fill_preserve vs fill** — `fill()` clears the path. Use `fill_preserve()`
   if you also want to stroke the same path.
3. **Surface must be flushed** — Call `surface.flush()` before
   `surface.write_to_png()` if you've done any direct pixel manipulation.
4. **ARGB32 byte order** — Cairo stores pixels as BGRA on little-endian
   systems. If converting to Pillow, use `"BGRA"` mode or swap channels.
5. **Font loading** — Cairo's built-in font selection is limited. For
   specific .ttf files, Pango+PangoCairo is the robust solution. If Pango
   isn't available, `select_font_face` with common names usually works.
6. **Transparency** — Use `FORMAT_ARGB32` for the surface to support alpha.
