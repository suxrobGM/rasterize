#!/usr/bin/env python3
"""Rasterize: Shared helpers for all engines.

Import these utilities in any generation script:
    from helpers import PALETTES, hex_to_rgb, contrast_ratio, ...
"""

import os

# === PATHS ===
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(SKILL_DIR, "assets", "fonts")


# === COLOR PALETTES ===

PALETTES = {
    "blue": {
        "primary": "#3b82f6",
        "accent": "#06b6d4",
        "bg_dark": "#0f172a",
        "bg_card": "#1e293b",
        "text": "#f8fafc",
        "text_muted": "#94a3b8",
        "border": "#334155",
    },
    "purple": {
        "primary": "#8b5cf6",
        "accent": "#a78bfa",
        "bg_dark": "#0c0a1a",
        "bg_card": "#1a1530",
        "text": "#f8fafc",
        "text_muted": "#a1a1aa",
        "border": "#2e2650",
    },
    "green": {
        "primary": "#10b981",
        "accent": "#34d399",
        "bg_dark": "#0a1a14",
        "bg_card": "#132a20",
        "text": "#f0fdf4",
        "text_muted": "#86efac",
        "border": "#1a3d2e",
    },
    "warm": {
        "primary": "#f59e0b",
        "accent": "#f97316",
        "bg_dark": "#1a1008",
        "bg_card": "#2a1f10",
        "text": "#fefce8",
        "text_muted": "#d4a373",
        "border": "#3d2e15",
    },
    "light": {
        "primary": "#2563eb",
        "accent": "#3b82f6",
        "bg_dark": "#ffffff",
        "bg_card": "#f8fafc",
        "text": "#0f172a",
        "text_muted": "#64748b",
        "border": "#e2e8f0",
    },
}

CATEGORICAL_COLORS = [
    "#3b82f6", "#f59e0b", "#10b981", "#ef4444",
    "#8b5cf6", "#ec4899", "#06b6d4", "#f97316",
    "#84cc16", "#14b8a6", "#f43f5e", "#a855f7",
]


# === COLOR UTILITIES ===

def hex_to_rgb(hex_color):
    """Convert '#3b82f6' to (59, 130, 246)."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def hex_to_rgba(hex_color, alpha=1.0):
    """Convert '#3b82f6' to (59, 130, 246, 255) or with custom alpha."""
    r, g, b = hex_to_rgb(hex_color)
    return (r, g, b, int(alpha * 255))


def hex_to_float(hex_color, alpha=1.0):
    """Convert '#3b82f6' to (0.23, 0.51, 0.96, 1.0) for Cairo."""
    r, g, b = hex_to_rgb(hex_color)
    return (r / 255, g / 255, b / 255, alpha)


def rgb_to_hex(r, g, b):
    """Convert (59, 130, 246) to '#3b82f6'."""
    return f"#{r:02x}{g:02x}{b:02x}"


def lerp_color(c1, c2, t):
    """Linearly interpolate between two RGB tuples."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def luminance(r, g, b):
    """Relative luminance per WCAG 2.0."""
    def channel(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(color1, color2):
    """WCAG contrast ratio between two RGB tuples. Returns float >= 1."""
    l1 = luminance(*color1)
    l2 = luminance(*color2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def ensure_readable(text_color_hex, bg_color_hex, min_ratio=4.5):
    """Check if text meets WCAG AA contrast against background."""
    tc = hex_to_rgb(text_color_hex)
    bc = hex_to_rgb(bg_color_hex)
    return contrast_ratio(tc, bc) >= min_ratio


# === FONT UTILITIES ===

def list_fonts():
    """List available font files."""
    if not os.path.exists(FONT_DIR):
        return []
    return sorted([
        f for f in os.listdir(FONT_DIR)
        if f.endswith((".ttf", ".otf"))
    ])


def font_path(filename):
    """Get the absolute path to a bundled font file."""
    path = os.path.join(FONT_DIR, filename)
    if not os.path.exists(path):
        available = list_fonts()
        raise FileNotFoundError(
            f"Font '{filename}' not found in {FONT_DIR}. "
            f"Available: {', '.join(available[:10])}"
        )
    return path


# === LAYOUT UTILITIES ===

def grid_positions(n_items, cols, cell_width, cell_height,
                   start_x=0, start_y=0, gap_x=0, gap_y=0):
    """Calculate (x, y) positions for a grid layout."""
    positions = []
    for i in range(n_items):
        row = i // cols
        col = i % cols
        x = start_x + col * (cell_width + gap_x)
        y = start_y + row * (cell_height + gap_y)
        positions.append((x, y))
    return positions


def center_in_rect(item_w, item_h, rect_x, rect_y, rect_w, rect_h):
    """Center an item within a rectangle. Returns (x, y)."""
    x = rect_x + (rect_w - item_w) / 2
    y = rect_y + (rect_h - item_h) / 2
    return (x, y)


# === SIZE PRESETS ===

SIZES = {
    # Social media
    "og_image":       (1200, 630),
    "twitter_card":   (1200, 628),
    "instagram_post": (1080, 1080),
    "instagram_story":(1080, 1920),
    "facebook_cover": (820, 312),
    "linkedin_post":  (1200, 627),
    "youtube_thumb":  (1280, 720),

    # Print (at 300 DPI, sizes in pixels)
    "a4_portrait":    (2480, 3508),
    "a4_landscape":   (3508, 2480),
    "letter":         (2550, 3300),
    "poster_24x36":   (7200, 10800),

    # Screen
    "hd":             (1920, 1080),
    "4k":             (3840, 2160),
    "icon_512":       (512, 512),
    "icon_256":       (256, 256),
    "favicon":        (32, 32),
}
