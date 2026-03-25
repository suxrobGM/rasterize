#!/usr/bin/env python3
"""Rasterize: Shared helpers for all engines.

Provides color utilities, font helpers, layout functions, and size presets
used across generation scripts.

Import these utilities in any generation script::

    from scripts.helpers import PALETTES, hex_to_rgb, contrast_ratio, font_path
"""

import os

# === PATHS ===

SKILL_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""Absolute path to the plugin root directory."""

FONT_DIR: str = os.path.join(SKILL_DIR, "assets", "fonts")
"""Absolute path to the bundled fonts directory."""


# === COLOR PALETTES ===

PALETTES: dict[str, dict[str, str]] = {
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
"""Named color palettes keyed by mood. Each contains primary, accent,
bg_dark, bg_card, text, text_muted, and border hex values."""

CATEGORICAL_COLORS: list[str] = [
    "#3b82f6",
    "#f59e0b",
    "#10b981",
    "#ef4444",
    "#8b5cf6",
    "#ec4899",
    "#06b6d4",
    "#f97316",
    "#84cc16",
    "#14b8a6",
    "#f43f5e",
    "#a855f7",
]
"""12 distinct colors for multi-series charts and categorical data."""


# === COLOR UTILITIES ===


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert a hex color string to an RGB tuple.

    Args:
        hex_color: Hex color like ``'#3b82f6'`` or ``'3b82f6'``.

    Returns:
        Tuple of (red, green, blue) integers in 0-255.
    """
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> tuple[int, int, int, int]:
    """Convert a hex color string to an RGBA tuple.

    Args:
        hex_color: Hex color like ``'#3b82f6'``.
        alpha: Opacity from 0.0 (transparent) to 1.0 (opaque).

    Returns:
        Tuple of (red, green, blue, alpha) with alpha scaled to 0-255.
    """
    r, g, b = hex_to_rgb(hex_color)
    return (r, g, b, int(alpha * 255))


def hex_to_float(hex_color: str, alpha: float = 1.0) -> tuple[float, float, float, float]:
    """Convert a hex color to Cairo-style normalized floats.

    Args:
        hex_color: Hex color like ``'#3b82f6'``.
        alpha: Opacity from 0.0 to 1.0.

    Returns:
        Tuple of (r, g, b, a) with each channel in 0.0-1.0.
    """
    r, g, b = hex_to_rgb(hex_color)
    return (r / 255, g / 255, b / 255, alpha)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert an RGB tuple to a hex color string.

    Args:
        r: Red channel (0-255).
        g: Green channel (0-255).
        b: Blue channel (0-255).

    Returns:
        Hex string like ``'#3b82f6'``.
    """
    return f"#{r:02x}{g:02x}{b:02x}"


def lerp_color(c1: tuple[int, ...], c2: tuple[int, ...], t: float) -> tuple[int, ...]:
    """Linearly interpolate between two RGB(A) tuples.

    Args:
        c1: Start color as an RGB or RGBA tuple.
        c2: End color as an RGB or RGBA tuple.
        t: Interpolation factor from 0.0 (c1) to 1.0 (c2).

    Returns:
        Interpolated color tuple with the same number of channels.
    """
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def luminance(r: int, g: int, b: int) -> float:
    """Calculate relative luminance per WCAG 2.0.

    Args:
        r: Red channel (0-255).
        g: Green channel (0-255).
        b: Blue channel (0-255).

    Returns:
        Relative luminance as a float between 0.0 and 1.0.
    """

    def channel(c: int) -> float:
        c_norm = c / 255
        return c_norm / 12.92 if c_norm <= 0.03928 else ((c_norm + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(color1: tuple[int, int, int], color2: tuple[int, int, int]) -> float:
    """Calculate WCAG contrast ratio between two RGB colors.

    Args:
        color1: First color as (r, g, b).
        color2: Second color as (r, g, b).

    Returns:
        Contrast ratio as a float >= 1.0. A ratio of 4.5+ passes WCAG AA
        for normal text; 3.0+ passes for large text.
    """
    l1 = luminance(*color1)
    l2 = luminance(*color2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def ensure_readable(text_color_hex: str, bg_color_hex: str, min_ratio: float = 4.5) -> bool:
    """Check if text meets WCAG AA contrast against a background.

    Args:
        text_color_hex: Text color as hex string.
        bg_color_hex: Background color as hex string.
        min_ratio: Minimum contrast ratio (default 4.5 for WCAG AA).

    Returns:
        True if the contrast ratio meets or exceeds ``min_ratio``.
    """
    tc = hex_to_rgb(text_color_hex)
    bc = hex_to_rgb(bg_color_hex)
    return contrast_ratio(tc, bc) >= min_ratio


# === FONT UTILITIES ===


def list_fonts() -> list[str]:
    """List available bundled font filenames.

    Returns:
        Sorted list of ``.ttf`` and ``.otf`` filenames in the fonts directory.
        Returns an empty list if the fonts directory does not exist.
    """
    if not os.path.exists(FONT_DIR):
        return []
    return sorted(f for f in os.listdir(FONT_DIR) if f.endswith((".ttf", ".otf")))


def font_path(filename: str) -> str:
    """Get the absolute path to a bundled font file.

    Args:
        filename: Font filename (e.g. ``'Outfit-Bold.ttf'``).

    Returns:
        Absolute path to the font file.

    Raises:
        FileNotFoundError: If the font file does not exist, with a message
            listing up to 10 available fonts.
    """
    path = os.path.join(FONT_DIR, filename)
    if not os.path.exists(path):
        available = list_fonts()
        raise FileNotFoundError(
            f"Font '{filename}' not found in {FONT_DIR}. Available: {', '.join(available[:10])}"
        )
    return path


# === LAYOUT UTILITIES ===


def grid_positions(
    n_items: int,
    cols: int,
    cell_width: float,
    cell_height: float,
    start_x: float = 0,
    start_y: float = 0,
    gap_x: float = 0,
    gap_y: float = 0,
) -> list[tuple[float, float]]:
    """Calculate (x, y) positions for items in a grid layout.

    Args:
        n_items: Total number of items to position.
        cols: Number of columns in the grid.
        cell_width: Width of each cell.
        cell_height: Height of each cell.
        start_x: X offset of the grid origin.
        start_y: Y offset of the grid origin.
        gap_x: Horizontal gap between cells.
        gap_y: Vertical gap between cells.

    Returns:
        List of (x, y) tuples, one per item, in row-major order.
    """
    positions: list[tuple[float, float]] = []
    for i in range(n_items):
        row = i // cols
        col = i % cols
        x = start_x + col * (cell_width + gap_x)
        y = start_y + row * (cell_height + gap_y)
        positions.append((x, y))
    return positions


def center_in_rect(
    item_w: float,
    item_h: float,
    rect_x: float,
    rect_y: float,
    rect_w: float,
    rect_h: float,
) -> tuple[float, float]:
    """Calculate the position to center an item within a rectangle.

    Args:
        item_w: Width of the item to center.
        item_h: Height of the item to center.
        rect_x: X coordinate of the rectangle's top-left corner.
        rect_y: Y coordinate of the rectangle's top-left corner.
        rect_w: Width of the rectangle.
        rect_h: Height of the rectangle.

    Returns:
        Tuple of (x, y) for the item's top-left corner when centered.
    """
    x = rect_x + (rect_w - item_w) / 2
    y = rect_y + (rect_h - item_h) / 2
    return (x, y)


# === SIZE PRESETS ===

SIZES: dict[str, tuple[int, int]] = {
    # Social media
    "og_image": (1200, 630),
    "twitter_card": (1200, 628),
    "instagram_post": (1080, 1080),
    "instagram_story": (1080, 1920),
    "facebook_cover": (820, 312),
    "linkedin_post": (1200, 627),
    "youtube_thumb": (1280, 720),
    # Print (at 300 DPI, sizes in pixels)
    "a4_portrait": (2480, 3508),
    "a4_landscape": (3508, 2480),
    "letter": (2550, 3300),
    "poster_24x36": (7200, 10800),
    # Screen
    "hd": (1920, 1080),
    "4k": (3840, 2160),
    "icon_512": (512, 512),
    "icon_256": (256, 256),
    "favicon": (32, 32),
}
"""Common image dimension presets as (width, height) tuples in pixels."""
