# Themes & Color Palettes

Shared color values used across all engines. Import from `scripts/helpers.py`
or copy the values directly.

## Dark theme (default)

| Token | Hex | Usage |
|-------|-----|-------|
| `bg_dark` | `#0f172a` | Page / figure background |
| `bg_card` | `#1e293b` | Card / axes / panel background |
| `border` | `#334155` | Borders, grid lines, dividers |
| `text` | `#f8fafc` | Primary text, titles |
| `text_muted` | `#94a3b8` | Secondary text, axis labels |
| `primary` | `#3b82f6` | Accent, links, highlights |
| `accent` | `#06b6d4` | Secondary accent |

### Matplotlib rcParams

```python
plt.rcParams.update({
    "figure.facecolor": "#0f172a",
    "axes.facecolor": "#1e293b",
    "axes.edgecolor": "#334155",
    "axes.labelcolor": "#e2e8f0",
    "text.color": "#e2e8f0",
    "xtick.color": "#94a3b8",
    "ytick.color": "#94a3b8",
    "grid.color": "#334155",
    "grid.alpha": 0.5,
})
```

### Plotly template

```python
go.Layout(
    paper_bgcolor="#0f172a",
    plot_bgcolor="#1e293b",
    font=dict(color="#e2e8f0"),
    xaxis=dict(gridcolor="#334155"),
    yaxis=dict(gridcolor="#334155"),
)
```

### CSS (Playwright)

```css
body { background: #0f172a; color: #f8fafc; }
.card { background: #1e293b; border: 1px solid #334155; }
```

### Cairo

```python
# Background
ctx.set_source_rgba(0.06, 0.09, 0.16, 1)  # #0f172a
# Card
ctx.set_source_rgba(0.12, 0.16, 0.23, 1)  # #1e293b
```

## Light theme

| Token | Hex |
|-------|-----|
| `bg_dark` | `#ffffff` |
| `bg_card` | `#f8fafc` |
| `border` | `#e2e8f0` |
| `text` | `#0f172a` |
| `text_muted` | `#64748b` |
| `primary` | `#2563eb` |

## Categorical palette (charts & data viz)

Use these 8 colors in order for multi-series charts:

```python
["#3b82f6", "#f59e0b", "#10b981", "#ef4444",
 "#8b5cf6", "#ec4899", "#06b6d4", "#f97316"]
```

Extended (12 colors) available in `helpers.CATEGORICAL_COLORS`.

## Sequential palette

```python
["#dbeafe", "#93c5fd", "#60a5fa", "#3b82f6",
 "#2563eb", "#1d4ed8", "#1e40af"]
```

## Diverging palette

```python
["#ef4444", "#f87171", "#fca5a5", "#fde2e2",
 "#d1fae5", "#6ee7b7", "#34d399", "#10b981"]
```

## Named palettes (helpers.py)

`PALETTES` dict provides complete palettes by mood: `"blue"`, `"purple"`,
`"green"`, `"warm"`, `"light"`. Each has `primary`, `accent`, `bg_dark`,
`bg_card`, `text`, `text_muted`, `border`.
