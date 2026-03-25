# Canvas, Scaling & Output

## Standard dimensions

```python
WIDTH, HEIGHT = 1200, 630       # Logical dimensions (1x)
SCALE = 2                       # Retina multiplier
W, H = WIDTH * SCALE, HEIGHT * SCALE   # Physical pixel dimensions
```

All engines default to 2× retina. Report dimensions to the user in
logical (1x) units.

### Common size presets

Available in `helpers.SIZES`:

| Name | Logical (w×h) | Use case |
|------|---------------|----------|
| `og_image` | 1200×630 | Open Graph / link previews |
| `twitter_card` | 1200×628 | Twitter cards |
| `instagram_post` | 1080×1080 | Instagram square posts |
| `instagram_story` | 1080×1920 | Instagram / TikTok stories |
| `youtube_thumb` | 1280×720 | YouTube thumbnails |
| `hd` | 1920×1080 | 1080p screen |
| `4k` | 3840×2160 | 4K screen |
| `icon_512` | 512×512 | App icons |
| `favicon` | 32×32 | Browser favicons |

## Scaling per engine

| Engine | How to apply 2× | Notes |
|--------|-----------------|-------|
| **Pillow** | `W, H = WIDTH*SCALE, HEIGHT*SCALE` — render at physical size | Multiply font sizes by SCALE too |
| **Cairo** | `ctx.scale(SCALE, SCALE)` after creating surface at `W×H` | Work in logical coords after scaling |
| **Matplotlib** | `"savefig.dpi": 300` (or `dpi=300` in `savefig()`) | `figsize` stays in inches |
| **Plotly** | `fig.write_image(..., scale=2)` | `width`/`height` are logical |
| **Playwright** | `device_scale_factor=scale` in `new_page()` | Viewport is logical; output is `W×H` |

## Saving output

Default to PNG. Use JPEG for photo-heavy output, WebP for smallest size.

### Per-engine save patterns

**Pillow**

```python
img.save(OUTPUT_PATH, "PNG", optimize=True)                    # PNG
rgb = Image.new("RGB", img.size, (255, 255, 255))             # JPEG (flatten alpha)
rgb.paste(img, mask=img.split()[3])
rgb.save(OUTPUT_PATH, "JPEG", quality=92)
img.save(OUTPUT_PATH, "WebP", quality=90, method=6)            # WebP
```

**Cairo**

```python
surface.write_to_png(OUTPUT_PATH)                              # PNG (native)
# JPEG/WebP: convert via Pillow
import io; from PIL import Image
buf = io.BytesIO(); surface.write_to_png(buf); buf.seek(0)
Image.open(buf).save(OUTPUT_PATH, "JPEG", quality=92)
```

**Matplotlib**

```python
fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight",
            facecolor=fig.get_facecolor(), pad_inches=0.3)
plt.close(fig)
```

**Plotly**

```python
fig.write_image(OUTPUT_PATH, width=1200, height=630, scale=2)
```

**Playwright**

```python
page.screenshot(path=OUTPUT_PATH, type="png")                  # PNG
page.screenshot(path=OUTPUT_PATH, type="jpeg", quality=92)     # JPEG
```

## Output directory

All generated files (scripts + images) go in `generated/` at the plugin root.
This directory is gitignored. See SKILL.md "Workspace" section for naming conventions.

```python
import os
PLUGIN_ROOT = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.join(PLUGIN_ROOT, "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(GENERATED_DIR, "my-image.png")
```
