# Matplotlib + Seaborn Engine Reference

Best for: statistical charts, scientific plots, data visualization,
histograms, scatter plots, line charts, bar charts, heatmaps, box plots,
violin plots, pair plots, and any publication-quality figure.

> **Setup**: See `shared/setup.md` | **Fonts**: See `shared/fonts.md`
> **Canvas & output**: See `shared/canvas.md` | **Themes & palettes**: See `shared/themes.md`

## Core Patterns

### Professional figure setup

```python
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend — ALWAYS set first
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Dark theme — see shared/themes.md for full rcParams and light theme
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
    "font.family": "sans-serif",
    "font.size": 12,
    "axes.titlesize": 16,
    "axes.labelsize": 13,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.3,
})

WIDTH, HEIGHT = 12, 7  # inches
fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT))
```

### Bar chart

```python
categories = ["Q1", "Q2", "Q3", "Q4"]
values = [42, 58, 35, 71]

bars = ax.bar(categories, values, color=PALETTE_CATEGORICAL[:len(categories)],
              width=0.6, edgecolor="none", zorder=3)

# Value labels on bars
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f"{val}", ha="center", va="bottom", fontsize=11,
            fontweight="bold", color="#e2e8f0")

ax.set_ylabel("Revenue ($M)")
ax.set_title("Quarterly Revenue 2025", fontweight="bold", pad=15)
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
```

### Line chart with filled area

```python
x = np.linspace(0, 12, 100)
y1 = np.sin(x) * 20 + 50
y2 = np.cos(x) * 15 + 45

ax.plot(x, y1, color="#3b82f6", linewidth=2.5, label="Product A", zorder=3)
ax.fill_between(x, y1, alpha=0.15, color="#3b82f6")

ax.plot(x, y2, color="#f59e0b", linewidth=2.5, label="Product B", zorder=3)
ax.fill_between(x, y2, alpha=0.15, color="#f59e0b")

ax.legend(frameon=False, loc="upper right")
```

### Seaborn integration

```python
import seaborn as sns
import pandas as pd

sns.set_theme(style="darkgrid", palette=PALETTE_CATEGORICAL)

# Heatmap
data = np.random.randn(8, 8)
sns.heatmap(data, annot=True, fmt=".1f", cmap="RdBu_r",
            center=0, linewidths=0.5, ax=ax,
            cbar_kws={"shrink": 0.8})

# Distribution
sns.histplot(data=df, x="value", hue="category", kde=True, ax=ax)

# Scatter with regression
sns.regplot(data=df, x="x", y="y", scatter_kws={"alpha": 0.6}, ax=ax)
```

### Multi-panel layouts

```python
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Dashboard Overview", fontsize=20, fontweight="bold", y=0.98)

# Plot on each axis
axes[0, 0].bar(...)
axes[0, 1].plot(...)
axes[1, 0].scatter(...)
axes[1, 1].pie(...)

plt.tight_layout(rect=[0, 0, 1, 0.95])
```

### Annotations and callouts

```python
# Annotate a specific point
ax.annotate("Peak", xy=(x_peak, y_peak), xytext=(x_peak+1, y_peak+10),
            arrowprops=dict(arrowstyle="->", color="#3b82f6", lw=1.5),
            fontsize=11, color="#3b82f6", fontweight="bold")

# Add a text box
props = dict(boxstyle="round,pad=0.4", facecolor="#1e293b",
             edgecolor="#334155", alpha=0.9)
ax.text(0.02, 0.98, "Source: Internal Data", transform=ax.transAxes,
        fontsize=9, verticalalignment="top", bbox=props, color="#94a3b8")
```

## Common Gotchas

1. **Always set `matplotlib.use("Agg")` before importing pyplot** —
   otherwise it tries to open a display and crashes in headless environments.
2. **DPI matters** — `fig.savefig(dpi=300)` overrides `figure.dpi`. Always
   set save DPI explicitly for consistent output resolution.
3. **`tight_layout` vs `bbox_inches="tight"`** — use both. `tight_layout()`
   adjusts subplot spacing; `bbox_inches="tight"` crops whitespace on save.
4. **Close figures** — `plt.close(fig)` prevents memory leaks when
   generating multiple images in one script.
5. **Font registration** — Custom fonts must be registered with
   `font_manager.fontManager.addfont()` BEFORE any figure is created.
6. **Transparent backgrounds** — Use `transparent=True` in `savefig()` if
   you need a transparent PNG for compositing.
