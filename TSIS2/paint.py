import pygame
import os
from datetime import datetime
from tools import flood_fill

pygame.init()

WIDTH = 1000
HEIGHT = 700
BAR = 120
CANVAS_HEIGHT = HEIGHT - BAR

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")
font = pygame.font.SysFont("arial", 17)
title_font = pygame.font.SysFont("arial", 23)

canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill((255, 255, 255))

colors = [(0, 0, 0), (255, 0, 0), (0, 160, 0), (0, 0, 255),
          (255, 210, 0), (255, 120, 0), (150, 0, 180),
          (255, 105, 180), (120, 120, 120)]
color = colors[0]

tool = "pencil"
brush_size = 5
drawing = False
start_pos = None
last_pos = None
typing = False
text_input = ""
text_pos = None
clock = pygame.time.Clock()


def draw_shape(surface, shape, start, end, draw_color, size):
    x1, y1 = start
    x2, y2 = end
    left, top = min(x1, x2), min(y1, y2)
    width, height = abs(x2 - x1), abs(y2 - y1)

    if shape == "line":
        pygame.draw.line(surface, draw_color, start, end, size)
    elif shape == "rect":
        pygame.draw.rect(surface, draw_color, (left, top, width, height), size)
    elif shape == "square":
        side = max(width, height)
        if x2 < x1:
            left = x1 - side
        if y2 < y1:
            top = y1 - side
        pygame.draw.rect(surface, draw_color, (left, top, side, side), size)
    elif shape == "circle":
        radius = int(((x2-x1)**2 + (y2-y1)**2)**0.5)
        pygame.draw.circle(surface, draw_color, start, radius, size)
    elif shape == "right_triangle":
        pygame.draw.polygon(surface, draw_color,
                            [(x1, y1), (x2, y2), (x1, y2)], size)
    elif shape == "triangle":
        side = max(width, height)
        points = [(x1, y1 + side), (x1 + side//2, y1),
                  (x1 + side, y1 + side)]
        pygame.draw.polygon(surface, draw_color, points, size)
    elif shape == "rhombus":
        points = [(x1 + width//2, y1), (x2, y1 + height//2),
                  (x1 + width//2, y2), (x1, y1 + height//2)]
        pygame.draw.polygon(surface, draw_color, points, size)


def save_canvas():
    os.makedirs("saved_drawings", exist_ok=True)
    filename = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, os.path.join("saved_drawings", filename))
    print("Saved:", filename)


def draw_toolbar():
    screen.fill((225, 225, 225))
    pygame.draw.rect(screen, (195, 195, 195), (0, 0, WIDTH, BAR))
    screen.blit(title_font.render("TSIS2 PAINT", True, (20, 20, 20)), (12, 5))
    line1 = "P Pencil  L Line  R Rectangle  C Circle  E Eraser  Q Square"
    line2 = "W Right Triangle  T Triangle  Y Rhombus  F Fill  X Text"
    line3 = "1 Small (2px)  2 Medium (5px)  3 Large (10px)  Ctrl+S Save"
    screen.blit(font.render(line1, True, (20, 20, 20)), (12, 37))
    screen.blit(font.render(line2, True, (20, 20, 20)), (12, 60))
    screen.blit(font.render(line3, True, (20, 20, 20)), (12, 83))
    screen.blit(font.render("Colors:", True, (20, 20, 20)), (12, 98))
    for i, c in enumerate(colors):
        rect = pygame.Rect(78 + i*32, 96, 25, 20)
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, (30, 30, 30), rect, 1)
        if c == color:
            pygame.draw.rect(screen, (255, 255, 255), rect.inflate(4, 4), 2)
    info = "Tool: " + tool + " | Brush: " + str(brush_size) + " px"
    screen.blit(font.render(info, True, (20, 20, 20)), (430, 98))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if typing:
                if event.key == pygame.K_RETURN:
                    if text_input:
                        text_surface = pygame.font.SysFont("arial", 24).render(
                            text_input, True, color)
                        canvas.blit(text_surface, text_pos)
                    typing = False
                    text_input = ""
                    text_pos = None
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_input = ""
                    text_pos = None
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif event.unicode and event.unicode.isprintable():
                    text_input += event.unicode
            else:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_r:
                    tool = "rect"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_q:
                    tool = "square"
                elif event.key == pygame.K_w:
                    tool = "right_triangle"
                elif event.key == pygame.K_t:
                    tool = "triangle"
                elif event.key == pygame.K_y:
                    tool = "rhombus"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_x:
                    tool = "text"
                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10
                elif event.key == pygame.K_s and (
                    pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_GUI)
                ):
                    save_canvas()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if my < BAR:
                if 78 <= mx < 78 + len(colors)*32 and 96 <= my <= 116:
                    color = colors[(mx - 78)//32]
            else:
                pos = (mx, my - BAR)
                if tool == "fill":
                    flood_fill(canvas, pos[0], pos[1], color)
                elif tool == "text":
                    text_pos = pos
                    text_input = ""
                    typing = True
                else:
                    drawing = True
                    start_pos = pos
                    last_pos = pos

        elif event.type == pygame.MOUSEMOTION and drawing:
            mx, my = event.pos
            if my >= BAR:
                pos = (mx, my - BAR)
                if tool == "pencil":
                    pygame.draw.line(canvas, color, last_pos, pos, brush_size)
                    last_pos = pos
                elif tool == "eraser":
                    pygame.draw.line(canvas, (255, 255, 255), last_pos, pos, brush_size)
                    last_pos = pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing:
                mx, my = event.pos
                end_pos = (mx, max(0, min(CANVAS_HEIGHT-1, my-BAR)))
                if tool not in ["pencil", "eraser"]:
                    draw_shape(canvas, tool, start_pos, end_pos, color, brush_size)
                drawing = False

    draw_toolbar()
    screen.blit(canvas, (0, BAR))

    if drawing and tool not in ["pencil", "eraser"]:
        mx, my = pygame.mouse.get_pos()
        if my >= BAR:
            preview = canvas.copy()
            draw_shape(preview, tool, start_pos, (mx, my-BAR), color, brush_size)
            screen.blit(preview, (0, BAR))

    if typing and text_pos is not None:
        text_surface = pygame.font.SysFont("arial", 24).render(
            text_input + "|", True, color)
        screen.blit(text_surface, (text_pos[0], text_pos[1] + BAR))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
