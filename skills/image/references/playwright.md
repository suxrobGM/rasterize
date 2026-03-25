# Playwright Engine Reference

Best for: complex layouts rendered from HTML/CSS, poster designs with
advanced typography, social media graphics with web fonts, UI mockups,
anything that benefits from the full power of CSS (flexbox, grid, shadows,
gradients, blend modes, backdrop-filter, clamp(), custom properties).

> **Setup**: See `shared/setup.md` | **Fonts**: See `shared/fonts.md`
> **Canvas & output**: See `shared/canvas.md` | **Themes**: See `shared/themes.md`

Additional: `pdm run playwright install chromium` must be run before first use.

## Core Patterns

### Basic HTML-to-PNG

```python
from playwright.sync_api import sync_playwright
import os

# See shared/canvas.md for dimension presets
WIDTH, HEIGHT = 1200, 630
SCALE = 2
OUTPUT_PATH = "/path/to/output.png"
FONT_DIR = "/path/to/rasterize/assets/fonts"  # See shared/fonts.md

def render_html_to_png(html_content, output_path, width, height, scale=2):
    """Render an HTML string to a PNG image."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=scale,
        )
        page.set_content(html_content, wait_until="networkidle")
        page.screenshot(path=output_path, type="png")
        browser.close()

html = """
<!DOCTYPE html>
<html>
<head>
<style>
  @font-face {
    font-family: 'Outfit';
    src: url('file:///path/to/rasterize/assets/fonts/Outfit-Bold.ttf');
    font-weight: 700;
  }
  @font-face {
    font-family: 'Outfit';
    src: url('file:///path/to/rasterize/assets/fonts/Outfit-Regular.ttf');
    font-weight: 400;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1200px;
    height: 630px;
    background: #0f172a;
    font-family: 'Outfit', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #f8fafc;
  }
</style>
</head>
<body>
  <h1>Hello, Rasterize!</h1>
</body>
</html>
"""

render_html_to_png(html, OUTPUT_PATH, WIDTH, HEIGHT, SCALE)
```

### Template pattern for social cards

```python
import html as html_lib

def social_card(title, subtitle, accent_color="#3b82f6", bg_color="#0f172a"):
    # Escape user-provided strings to prevent HTML injection
    safe_title = html_lib.escape(title)
    safe_subtitle = html_lib.escape(subtitle)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
      @font-face {{
        font-family: 'Heading';
        src: url('file://{FONT_DIR}/Outfit-Bold.ttf');
        font-weight: 700;
      }}
      @font-face {{
        font-family: 'Body';
        src: url('file://{FONT_DIR}/InstrumentSans-Regular.ttf');
        font-weight: 400;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      body {{
        width: 1200px; height: 630px;
        background: {bg_color};
        font-family: 'Body', system-ui, sans-serif;
        display: flex; flex-direction: column;
        justify-content: center;
        padding: 80px;
        position: relative; overflow: hidden;
      }}
      /* Decorative gradient orb */
      body::before {{
        content: '';
        position: absolute;
        width: 600px; height: 600px;
        border-radius: 50%;
        background: radial-gradient(circle, {accent_color}33 0%, transparent 70%);
        top: -200px; right: -100px;
      }}
      h1 {{
        font-family: 'Heading', system-ui;
        font-size: 56px; line-height: 1.15;
        color: #f8fafc;
        max-width: 700px;
        margin-bottom: 20px;
      }}
      p {{
        font-size: 22px; color: #94a3b8;
        max-width: 600px;
      }}
      .accent-bar {{
        width: 60px; height: 4px;
        background: {accent_color};
        border-radius: 2px;
        margin-bottom: 24px;
      }}
    </style>
    </head>
    <body>
      <div class="accent-bar"></div>
      <h1>{safe_title}</h1>
      <p>{safe_subtitle}</p>
    </body>
    </html>
    """
```

### Advanced CSS techniques available

Because Playwright renders through real Chromium, you get full CSS support:

```css
/* Glass morphism */
.card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
}

/* CSS Grid layouts */
.dashboard {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: auto 1fr;
  gap: 16px;
}

/* Gradient text */
.gradient-text {
  background: linear-gradient(135deg, #3b82f6, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Noise texture overlay */
.noise::after {
  content: '';
  position: absolute; inset: 0;
  background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
}

/* Complex shadows */
.elevated {
  box-shadow:
    0 1px 2px rgba(0,0,0,0.1),
    0 4px 8px rgba(0,0,0,0.1),
    0 16px 32px rgba(0,0,0,0.15);
}
```

### Capturing specific elements

```python
# Screenshot just one element instead of full page
page.set_content(html, wait_until="networkidle")
element = page.query_selector(".card")
element.screenshot(path=OUTPUT_PATH)
```

### Waiting for fonts and assets to load

```python
page.set_content(html, wait_until="networkidle")
# Wait for all fonts to finish loading (must use async evaluation)
page.evaluate("async () => { await document.fonts.ready; }")
# Extra safety margin for font rasterization
page.wait_for_timeout(500)
page.screenshot(path=OUTPUT_PATH)
```

### Injecting dynamic data

```python
import json

def render_data_card(data_dict):
    data_json = json.dumps(data_dict)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><style>/* ... */</style></head>
    <body>
      <div id="app"></div>
      <script>
        const data = {data_json};
        const app = document.getElementById('app');
        // Build DOM safely — use textContent instead of innerHTML
        // to prevent XSS from data values
        data.items.forEach(item => {{
          const el = document.createElement('div');
          el.className = 'card';
          const h3 = document.createElement('h3');
          h3.textContent = item.title;
          const p = document.createElement('p');
          p.textContent = item.value;
          el.appendChild(h3);
          el.appendChild(p);
          app.appendChild(el);
        }});
      </script>
    </body>
    </html>
    """
    render_html_to_png(html, OUTPUT_PATH, 1200, 630)
```

## Common Gotchas

1. **`playwright install chromium`** — Must be run before first use.
   Without the browser binary, Playwright won't launch.
2. **Font loading** — Use `file://` absolute paths in `@font-face`. Relative
   paths don't work because the HTML is loaded via `set_content`, not from
   a file URL. Wait with `page.evaluate("async () => { await document.fonts.ready; }")`,
   then add `wait_for_timeout(500)` as a safety margin.
3. **Viewport vs content size** — The viewport determines the "window" size.
   Content that overflows is clipped unless you use `full_page=True`.
4. **`device_scale_factor`** — This is the retina multiplier. `scale=2`
   gives 2× pixel density. The output PNG will be `width*2 × height*2`.
5. **Memory** — Chromium is heavy. For batch generation, reuse the browser
   instance and create new pages instead of launching new browsers.
6. **Inline everything** — Since content is loaded via `set_content`, all
   CSS and JS must be inline or use absolute `file://` or `https://` URLs.
   No relative paths work.
7. **wait_until** — Use `"networkidle"` to ensure all resources are loaded
   before screenshotting. For pages with JS rendering, add explicit waits.
