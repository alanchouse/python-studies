from collections import deque
from datetime import datetime
import math

import pygame

from tools import (
    WIDTH,
    HEIGHT,
    TOOLBAR_HEIGHT,
    CANVAS_BG,
    UI_BG,
    UI_BORDER,
    TEXT_COLOR,
    PREVIEW_COLOR,
    build_tool_buttons,
    build_size_buttons,
    build_color_buttons,
)


def clamp_canvas_point(pos):
    x, y = pos
    x = max(0, min(WIDTH - 1, x))
    y = max(TOOLBAR_HEIGHT, min(HEIGHT - 1, y))
    return x, y


def to_canvas_coords(pos):
    x, y = clamp_canvas_point(pos)
    return x, y - TOOLBAR_HEIGHT


def draw_rect_shape(surface, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    rect = pygame.Rect(left, top, width, height)
    if rect.width and rect.height:
        pygame.draw.rect(surface, color, rect, thickness)


def draw_square(surface, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))
    x = x1 if x2 >= x1 else x1 - side
    y = y1 if y2 >= y1 else y1 - side
    rect = pygame.Rect(x, y, side, side)
    if side > 0:
        pygame.draw.rect(surface, color, rect, thickness)


def draw_circle_shape(surface, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    radius = int(math.hypot(x2 - x1, y2 - y1))
    if radius > 0:
        pygame.draw.circle(surface, color, start, radius, thickness)


def draw_right_triangle(surface, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, thickness)


def draw_equilateral_triangle(surface, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    side = max(1, abs(x2 - x1))
    height = int(side * math.sqrt(3) / 2)
    direction = 1 if y2 >= y1 else -1
    p1 = (x1, y1)
    p2 = (x1 + side, y1)
    p3 = (x1 + side // 2, y1 + direction * height)
    pygame.draw.polygon(surface, color, [p1, p2, p3], thickness)


def draw_rhombus(surface, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
    pygame.draw.polygon(surface, color, points, thickness)


def draw_shape(surface, tool, color, start, end, thickness):
    if tool == "line":
        pygame.draw.line(surface, color, start, end, thickness)
    elif tool == "rect":
        draw_rect_shape(surface, color, start, end, thickness)
    elif tool == "circle":
        draw_circle_shape(surface, color, start, end, thickness)
    elif tool == "square":
        draw_square(surface, color, start, end, thickness)
    elif tool == "rtri":
        draw_right_triangle(surface, color, start, end, thickness)
    elif tool == "etri":
        draw_equilateral_triangle(surface, color, start, end, thickness)
    elif tool == "rhombus":
        draw_rhombus(surface, color, start, end, thickness)


def flood_fill(canvas, start_pos, new_color):
    width, height = canvas.get_size()
    sx, sy = start_pos
    if not (0 <= sx < width and 0 <= sy < height):
        return

    target_color = canvas.get_at((sx, sy))
    new_rgba = (*new_color, 255)
    if target_color == new_rgba:
        return

    # Classic BFS flood-fill with 4-neighbour connectivity.
    queue = deque([(sx, sy)])
    while queue:
        x, y = queue.popleft()
        if canvas.get_at((x, y)) != target_color:
            continue
        canvas.set_at((x, y), new_rgba)
        if x > 0:
            queue.append((x - 1, y))
        if x < width - 1:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y < height - 1:
            queue.append((x, y + 1))


def save_canvas(canvas):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{stamp}.png"
    pygame.image.save(canvas, filename)
    return filename


def draw_ui(screen, font, state, tool_buttons, size_buttons, color_buttons):
    pygame.draw.rect(screen, UI_BG, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, UI_BORDER, (0, TOOLBAR_HEIGHT - 1), (WIDTH, TOOLBAR_HEIGHT - 1), 2)

    for button in tool_buttons:
        active = button["name"] == state["tool"]
        bg = (180, 220, 255) if active else (248, 248, 248)
        pygame.draw.rect(screen, bg, button["rect"])
        pygame.draw.rect(screen, UI_BORDER, button["rect"], 1)
        text = font.render(button["label"], True, TEXT_COLOR)
        screen.blit(text, (button["rect"].x + 6, button["rect"].y + 7))

    for button in size_buttons:
        active = button["size"] == state["size"]
        bg = (180, 220, 255) if active else (248, 248, 248)
        pygame.draw.rect(screen, bg, button["rect"])
        pygame.draw.rect(screen, UI_BORDER, button["rect"], 1)
        text = font.render(button["label"], True, TEXT_COLOR)
        screen.blit(text, (button["rect"].x + 10, button["rect"].y + 7))

    for button in color_buttons:
        pygame.draw.rect(screen, button["color"], button["rect"])
        border = (20, 20, 20) if button["color"] == state["color"] else UI_BORDER
        pygame.draw.rect(screen, border, button["rect"], 2)

    pygame.draw.rect(screen, state["color"], (WIDTH - 70, 90, 52, 30))
    pygame.draw.rect(screen, UI_BORDER, (WIDTH - 70, 90, 52, 30), 2)

    hint = "Ctrl+S save | Enter confirm text | Esc cancel text"
    hint_text = font.render(hint, True, (70, 70, 70))
    screen.blit(hint_text, (12, TOOLBAR_HEIGHT - 28))


def handle_hotkeys(event, state):
    if event.key == pygame.K_1:
        state["size"] = 2
    elif event.key == pygame.K_2:
        state["size"] = 5
    elif event.key == pygame.K_3:
        state["size"] = 10
    elif event.key == pygame.K_p:
        state["tool"] = "pencil"
    elif event.key == pygame.K_l:
        state["tool"] = "line"
    elif event.key == pygame.K_r:
        state["tool"] = "rect"
    elif event.key == pygame.K_c:
        state["tool"] = "circle"
    elif event.key == pygame.K_q:
        state["tool"] = "square"
    elif event.key == pygame.K_t:
        state["tool"] = "rtri"
    elif event.key == pygame.K_e:
        state["tool"] = "etri"
    elif event.key == pygame.K_h:
        state["tool"] = "rhombus"
    elif event.key == pygame.K_f:
        state["tool"] = "fill"
    elif event.key == pygame.K_x:
        state["tool"] = "text"
    elif event.key == pygame.K_z:
        state["tool"] = "eraser"


def main():
    pygame.init()
    pygame.display.set_caption("TSIS2 Paint")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont("Arial", 16)
    text_font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()

    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(CANVAS_BG)

    tool_buttons = build_tool_buttons()
    size_buttons = build_size_buttons()
    color_buttons = build_color_buttons()

    state = {
        "tool": "pencil",
        "color": (0, 0, 0),
        "size": 2,
        "drawing": False,
        "start": None,
        "last": None,
        "text_active": False,
        "text_value": "",
        "text_pos": (0, 0),
        "saved_name": "",
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                mod = pygame.key.get_mods()
                if event.key == pygame.K_s and (mod & pygame.KMOD_CTRL):
                    state["saved_name"] = save_canvas(canvas)
                    continue

                if state["text_active"]:
                    if event.key == pygame.K_RETURN:
                        if state["text_value"]:
                            text_surface = text_font.render(state["text_value"], True, state["color"])
                            canvas.blit(text_surface, state["text_pos"])
                        state["text_active"] = False
                        state["text_value"] = ""
                    elif event.key == pygame.K_ESCAPE:
                        state["text_active"] = False
                        state["text_value"] = ""
                    elif event.key == pygame.K_BACKSPACE:
                        state["text_value"] = state["text_value"][:-1]
                    elif event.unicode.isprintable():
                        state["text_value"] += event.unicode
                else:
                    handle_hotkeys(event, state)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                handled = False
                # Top toolbar buttons have priority over drawing area clicks.
                for button in tool_buttons:
                    if button["rect"].collidepoint(pos):
                        state["tool"] = button["name"]
                        handled = True
                        break
                if handled:
                    continue

                for button in size_buttons:
                    if button["rect"].collidepoint(pos):
                        state["size"] = button["size"]
                        handled = True
                        break
                if handled:
                    continue

                for button in color_buttons:
                    if button["rect"].collidepoint(pos):
                        state["color"] = button["color"]
                        handled = True
                        break
                if handled or pos[1] < TOOLBAR_HEIGHT:
                    continue

                cx, cy = to_canvas_coords(pos)
                if state["tool"] == "fill":
                    flood_fill(canvas, (cx, cy), state["color"])
                elif state["tool"] == "text":
                    state["text_active"] = True
                    state["text_value"] = ""
                    state["text_pos"] = (cx, cy)
                else:
                    state["drawing"] = True
                    state["start"] = (cx, cy)
                    state["last"] = (cx, cy)
                    if state["tool"] in ("pencil", "eraser"):
                        paint_color = CANVAS_BG if state["tool"] == "eraser" else state["color"]
                        pygame.draw.circle(canvas, paint_color, (cx, cy), max(1, state["size"] // 2))

            elif event.type == pygame.MOUSEMOTION and state["drawing"]:
                cx, cy = to_canvas_coords(event.pos)
                if state["tool"] in ("pencil", "eraser"):
                    # Freehand drawing is simulated by connecting mouse points.
                    paint_color = CANVAS_BG if state["tool"] == "eraser" else state["color"]
                    pygame.draw.line(canvas, paint_color, state["last"], (cx, cy), state["size"])
                state["last"] = (cx, cy)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and state["drawing"]:
                cx, cy = to_canvas_coords(event.pos)
                if state["tool"] not in ("pencil", "eraser"):
                    draw_shape(canvas, state["tool"], state["color"], state["start"], (cx, cy), state["size"])
                state["drawing"] = False
                state["start"] = None
                state["last"] = None

        screen.fill(CANVAS_BG)
        draw_ui(screen, font, state, tool_buttons, size_buttons, color_buttons)
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        if state["drawing"] and state["tool"] not in ("pencil", "eraser"):
            # Draw preview on a temporary copy, commit only on mouse release.
            preview_canvas = canvas.copy()
            mx, my = to_canvas_coords(pygame.mouse.get_pos())
            draw_shape(preview_canvas, state["tool"], PREVIEW_COLOR, state["start"], (mx, my), state["size"])
            screen.blit(preview_canvas, (0, TOOLBAR_HEIGHT))

        if state["text_active"]:
            tx, ty = state["text_pos"]
            text_to_show = state["text_value"] + "|"
            text_surface = text_font.render(text_to_show, True, state["color"])
            screen.blit(text_surface, (tx, ty + TOOLBAR_HEIGHT))

        if state["saved_name"]:
            saved_info = font.render(f"Saved: {state['saved_name']}", True, (20, 110, 20))
            screen.blit(saved_info, (WIDTH - 330, TOOLBAR_HEIGHT - 28))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
