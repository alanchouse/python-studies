import pygame


WIDTH, HEIGHT = 1200, 800
TOOLBAR_HEIGHT = 170
CANVAS_BG = (255, 255, 255)
UI_BG = (235, 235, 235)
UI_BORDER = (180, 180, 180)
TEXT_COLOR = (30, 30, 30)
PREVIEW_COLOR = (120, 120, 120)

TOOLS = [
    ("pencil", "Pencil (P)"),
    ("line", "Line (L)"),
    ("rect", "Rect (R)"),
    ("circle", "Circle (C)"),
    ("square", "Square (Q)"),
    ("rtri", "R.Tri (T)"),
    ("etri", "E.Tri (E)"),
    ("rhombus", "Rhombus (H)"),
    ("fill", "Fill (F)"),
    ("text", "Text (X)"),
    ("eraser", "Eraser (Z)"),
]

SIZES = [
    (2, "1: Small"),
    (5, "2: Medium"),
    (10, "3: Large"),
]

PALETTE = [
    (0, 0, 0),
    (255, 255, 255),
    (255, 0, 0),
    (0, 170, 0),
    (0, 70, 255),
    (255, 170, 0),
    (140, 0, 180),
    (0, 170, 170),
]


def build_tool_buttons():
    buttons = []
    x, y = 12, 12
    w, h = 96, 30
    gap = 6
    for name, label in TOOLS:
        rect = pygame.Rect(x, y, w, h)
        buttons.append({"name": name, "label": label, "rect": rect})
        x += w + gap
        if x + w > WIDTH - 12:
            x = 12
            y += h + gap
    return buttons


def build_size_buttons():
    buttons = []
    x = WIDTH - 320
    y = 50
    w, h = 95, 30
    gap = 8
    for size, label in SIZES:
        rect = pygame.Rect(x, y, w, h)
        buttons.append({"size": size, "label": label, "rect": rect})
        x += w + gap
    return buttons


def build_color_buttons():
    buttons = []
    x = WIDTH - 320
    y = 92
    swatch = 24
    gap = 6
    for color in PALETTE:
        rect = pygame.Rect(x, y, swatch, swatch)
        buttons.append({"color": color, "rect": rect})
        x += swatch + gap
    return buttons
