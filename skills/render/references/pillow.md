# Pillow Engine Reference

Best for: photo manipulation, compositing, filters, pixel-level operations,
texture generation, simple graphics with raster effects.

> **Setup**: See `shared/setup.md` | **Fonts**: See `shared/fonts.md`
> **Canvas & output**: See `shared/canvas.md` | **Themes**: See `shared/themes.md`

## Core Patterns

### Basic canvas setup

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math

# See shared/canvas.md for dimension presets
WIDTH, HEIGHT = 1200, 630
SCALE = 2
W, H = WIDTH * SCALE, HEIGHT * SCALE

img = Image.new("RGBA", (W, H), (15, 23, 42, 255))
draw = ImageDraw.Draw(img)
```

### Anti-aliased shapes (supersample trick)

Pillow's ImageDraw doesn't anti-alias. To get smooth edges, render at
4× then downscale:

```python
def smooth_circle(radius, fill, bg=(0,0,0,0)):
    """Create an anti-aliased circle."""
    ss = 4  # supersample factor
    size = radius * 2 * ss
    tmp = Image.new("RGBA", (size, size), bg)
    d = ImageDraw.Draw(tmp)
    d.ellipse([0, 0, size-1, size-1], fill=fill)
    return tmp.resize((radius*2, radius*2), Image.LANCZOS)
```

### Gradient backgrounds

```python
def linear_gradient(w, h, start_color, end_color, direction="vertical"):
    """Create a smooth gradient image."""
    img = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(img)  # Create once, reuse for all lines
    span = h if direction == "vertical" else w
    for i in range(span):
        t = i / span
        r = int(start_color[0] + (end_color[0] - start_color[0]) * t)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * t)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * t)
        a = int(start_color[3] + (end_color[3] - start_color[3]) * t) if len(start_color) > 3 else 255
        if direction == "vertical":
            draw.line([(0, i), (w, i)], fill=(r, g, b, a))
        else:
            draw.line([(i, 0), (i, h)], fill=(r, g, b, a))
    return img
```

### Radial gradient (NumPy accelerated)

```python
import numpy as np

def radial_gradient(w, h, center_color, edge_color, center=(0.5, 0.5)):
    """Create a radial gradient. center is normalized (0-1)."""
    cx, cy = int(w * center[0]), int(h * center[1])
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
    max_dist = np.sqrt(max(cx, w-cx)**2 + max(cy, h-cy)**2)
    t = np.clip(dist / max_dist, 0, 1)

    img_arr = np.zeros((h, w, 4), dtype=np.uint8)
    for c in range(min(len(center_color), len(edge_color))):
        img_arr[:, :, c] = (center_color[c] * (1-t) + edge_color[c] * t).astype(np.uint8)
    if len(center_color) < 4:
        img_arr[:, :, 3] = 255

    return Image.fromarray(img_arr, "RGBA")
```

### Drop shadows

```python
def add_shadow(img, offset=(10, 10), blur_radius=20, shadow_color=(0,0,0,128)):
    """Add a drop shadow behind an RGBA image."""
    shadow = Image.new("RGBA", img.size, (0,0,0,0))
    alpha = img.split()[3]
    shadow_layer = Image.new("RGBA", img.size, shadow_color)
    shadow_layer.putalpha(alpha)
    shadow.paste(shadow_layer, offset)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
    shadow.paste(img, (0, 0), img)
    return shadow
```

### Text with bounding box measurement

```python
def draw_text_centered(draw, text, font, y, canvas_width, fill=(255,255,255)):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (canvas_width - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
```

### Rounded rectangles

```python
def rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    """Draw a rounded rectangle. xy = (x0, y0, x1, y1)."""
    # Pillow 9.0+ has native rounded_rectangle
    draw.rounded_rectangle(xy, radius=radius, fill=fill,
                            outline=outline, width=width)
```

### Compositing layers

```python
# Paste with alpha compositing
background = Image.new("RGBA", (W, H), (15, 23, 42, 255))
foreground = Image.open("overlay.png").convert("RGBA")
background = Image.alpha_composite(background, foreground)

# Paste at specific position
canvas = Image.new("RGBA", (W, H), (0,0,0,0))
canvas.paste(element, (x, y), element)  # 3rd arg = mask
```

## Common Gotchas

1. **ImageDraw doesn't anti-alias** — always supersample or use
   `rounded_rectangle` (Pillow 9.0+) for shapes.
2. **Text rendering** — Pillow's text is decent but not sub-pixel rendered.
   For important typography, consider Cairo or Playwright instead.
3. **Color mode** — Use `"RGBA"` when you need transparency. Convert to
   `"RGB"` before saving as JPEG.
4. **Font size** — Remember to multiply by SCALE when rendering at retina.
5. **Pixel loops are slow** — Use NumPy arrays for per-pixel operations
   instead of `img.putpixel()` in loops.
