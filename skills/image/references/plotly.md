# Plotly Engine Reference

Best for: complex/interactive-looking data visualizations exported as static
images — annotated dashboards, rich statistical plots, 3D surfaces, maps,
sunburst/treemap diagrams, and anything that benefits from Plotly's polished
default styling.

> **Setup**: See `shared/setup.md` | **Fonts**: See `shared/fonts.md`
> **Canvas & output**: See `shared/canvas.md` | **Themes & palettes**: See `shared/themes.md`

**kaleido** is required for static image export (no browser needed).

## Core Patterns

### Basic figure setup

```python
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

# Dark theme — see shared/themes.md for color tokens and Plotly template
DARK_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="#0f172a",
        plot_bgcolor="#1e293b",
        font=dict(color="#e2e8f0", family="Inter, sans-serif"),
        title=dict(font=dict(size=22, color="#f8fafc")),
        xaxis=dict(gridcolor="#334155", linecolor="#334155", zerolinecolor="#334155"),
        yaxis=dict(gridcolor="#334155", linecolor="#334155", zerolinecolor="#334155"),
        colorway=["#3b82f6", "#f59e0b", "#10b981", "#ef4444",
                  "#8b5cf6", "#ec4899", "#06b6d4", "#f97316"],
    )
)

fig = go.Figure()
fig.update_layout(template=DARK_TEMPLATE)
```

### Plotly Express (quick charts)

```python
import pandas as pd

df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [42, 58, 35, 71, 63, 80],
    "Costs": [30, 35, 28, 45, 40, 50],
})

# Bar chart
fig = px.bar(df, x="Month", y="Revenue",
             color_discrete_sequence=["#3b82f6"],
             title="Monthly Revenue")

# Line chart
fig = px.line(df, x="Month", y=["Revenue", "Costs"],
              title="Revenue vs Costs")

# Scatter
fig = px.scatter(df, x="Costs", y="Revenue", size="Revenue",
                 color="Month", title="Cost-Revenue Analysis")
```

### Graph Objects (full control)

```python
fig = go.Figure()

fig.add_trace(go.Bar(
    x=categories, y=values,
    marker=dict(color="#3b82f6", line=dict(width=0)),
    text=values, textposition="outside",
    textfont=dict(color="#e2e8f0", size=13),
    name="Revenue"
))

fig.update_layout(
    title=dict(text="Quarterly Revenue", x=0.5),
    xaxis_title="Quarter",
    yaxis_title="Revenue ($M)",
    showlegend=False,
    margin=dict(l=60, r=30, t=80, b=50),
    width=1200, height=630,
)
```

### Multi-subplot dashboard

```python
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Revenue", "Users", "Conversion", "Retention"),
    specs=[[{"type": "bar"}, {"type": "scatter"}],
           [{"type": "pie"}, {"type": "heatmap"}]],
    vertical_spacing=0.12,
    horizontal_spacing=0.08,
)

fig.add_trace(go.Bar(x=months, y=revenue), row=1, col=1)
fig.add_trace(go.Scatter(x=months, y=users, mode="lines+markers"), row=1, col=2)
fig.add_trace(go.Pie(labels=segments, values=conversions), row=2, col=1)
fig.add_trace(go.Heatmap(z=retention_matrix), row=2, col=2)

fig.update_layout(height=800, width=1400, title_text="Business Dashboard")
```

### Annotations and shapes

```python
fig.add_annotation(
    x="Mar", y=71, text="Record high!",
    showarrow=True, arrowhead=2, arrowcolor="#3b82f6",
    font=dict(size=13, color="#3b82f6"),
    bgcolor="#1e293b", bordercolor="#3b82f6",
)

# Horizontal reference line
fig.add_hline(y=50, line_dash="dash", line_color="#94a3b8",
              annotation_text="Target", annotation_position="top right")

# Shaded region
fig.add_vrect(x0="Apr", x1="Jun", fillcolor="#3b82f6",
              opacity=0.1, line_width=0)
```

### 3D plots

```python
fig = go.Figure(data=[go.Surface(z=z_data, colorscale="Viridis")])
fig.update_layout(
    scene=dict(
        xaxis_title="X", yaxis_title="Y", zaxis_title="Z",
        bgcolor="#1e293b",
    ),
    width=1000, height=700,
)
```

### Using custom fonts (Plotly-specific)

Plotly renders fonts via the system font stack (kaleido). Bundled fonts
must be copied to the OS font directory before they can be used:

```python
import shutil, os, sys, subprocess

FONT_DIR = "/path/to/rasterize/assets/fonts"

def install_fonts_for_plotly():
    """Copy bundled fonts to the OS font directory."""
    if sys.platform == "win32":
        local_fonts = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts")
    elif sys.platform == "darwin":
        local_fonts = os.path.expanduser("~/Library/Fonts")
    else:
        local_fonts = os.path.expanduser("~/.local/share/fonts")

    os.makedirs(local_fonts, exist_ok=True)
    for f in os.listdir(FONT_DIR):
        if f.endswith(".ttf"):
            shutil.copy2(os.path.join(FONT_DIR, f), local_fonts)

    # Rebuild font cache on Linux (not needed on Windows/macOS)
    if sys.platform not in ("win32", "darwin"):
        subprocess.run(["fc-cache", "-f"], capture_output=True)

install_fonts_for_plotly()
fig.update_layout(font=dict(family="Outfit"))
```

## Common Gotchas

1. **kaleido is required** — Without it, `write_image` won't work. Always
   install plotly AND kaleido together.
2. **scale parameter** — `scale=2` in `write_image` gives retina output.
   The `width` and `height` are logical pixels.
3. **Font availability** — Plotly/kaleido renders fonts via the system font
   stack. Custom fonts must be copied to the OS font directory (see the
   `install_fonts_for_plotly()` helper above). On Linux, run `fc-cache -f`
   after copying; on Windows/macOS this is not needed.
4. **Large datasets** — For 100k+ data points, Plotly can be slow to
   render. Consider downsampling or switching to Matplotlib.
5. **subplot types** — Each subplot cell needs a `type` in the `specs`
   parameter if it's not the default "xy" (e.g., "pie", "heatmap", "scene").
6. **Image format detection** — `write_image` infers format from the file
   extension. If using a stream, specify `format=` explicitly.
