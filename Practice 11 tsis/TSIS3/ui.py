import pygame


WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (95, 95, 95)
BLUE = (90, 145, 255)
GREEN = (79, 176, 103)


class Button:
    def __init__(self, rect: pygame.Rect, label: str):
        self.rect = rect
        self.label = label

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, active: bool = False) -> None:
        color = BLUE if active else GRAY
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, width=2, border_radius=8)
        text = font.render(self.label, True, WHITE)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def clicked(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def draw_title(surface: pygame.Surface, title_font: pygame.font.Font, text: str) -> None:
    header = title_font.render(text, True, WHITE)
    surface.blit(header, header.get_rect(center=(surface.get_width() // 2, 70)))


def draw_panel(surface: pygame.Surface, rect: pygame.Rect) -> None:
    pygame.draw.rect(surface, (45, 45, 45), rect, border_radius=12)
    pygame.draw.rect(surface, WHITE, rect, width=2, border_radius=12)


def draw_input_box(
    surface: pygame.Surface,
    font: pygame.font.Font,
    label: str,
    value: str,
    rect: pygame.Rect,
    active: bool,
) -> None:
    color = GREEN if active else WHITE
    pygame.draw.rect(surface, BLACK, rect, border_radius=8)
    pygame.draw.rect(surface, color, rect, width=2, border_radius=8)
    caption = font.render(label, True, WHITE)
    surface.blit(caption, (rect.x, rect.y - 26))
    typed = font.render(value if value else "_", True, WHITE)
    surface.blit(typed, (rect.x + 10, rect.y + 8))
