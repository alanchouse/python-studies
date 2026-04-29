from __future__ import annotations

import json
import math
from pathlib import Path
from array import array

import pygame

from config import DB_CONFIG, FPS, SETTINGS_PATH, WINDOW_HEIGHT, WINDOW_WIDTH
from db import Database
from game import SnakeGame


DEFAULT_SETTINGS = {
    "snake_color": [40, 210, 120],
    "grid": True,
    "sound": False,
}

SNAKE_COLORS = {
    "Green": [40, 210, 120],
    "Blue": [80, 160, 255],
    "Yellow": [255, 210, 70],
    "Purple": [180, 100, 255],
}


class Button:
    def __init__(self, rect: pygame.Rect, text: str):
        self.rect = rect
        self.text = text

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, active: bool = False) -> None:
        bg = (95, 130, 245) if active else (65, 65, 65)
        pygame.draw.rect(screen, bg, self.rect, border_radius=9)
        pygame.draw.rect(screen, (240, 240, 240), self.rect, width=2, border_radius=9)
        label = font.render(self.text, True, (245, 245, 245))
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event: pygame.event.Event) -> bool:
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def load_settings(path: Path) -> dict:
    if not path.exists():
        return DEFAULT_SETTINGS.copy()
    try:
        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError):
        return DEFAULT_SETTINGS.copy()
    result = DEFAULT_SETTINGS.copy()
    if isinstance(raw, dict):
        result.update({k: v for k, v in raw.items() if k in result})
    if not isinstance(result["snake_color"], list) or len(result["snake_color"]) != 3:
        result["snake_color"] = DEFAULT_SETTINGS["snake_color"][:]
    result["grid"] = bool(result["grid"])
    result["sound"] = bool(result["sound"])
    return result


def save_settings(path: Path, settings: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=True, indent=2)


def draw_input(screen: pygame.Surface, font: pygame.font.Font, label: str, value: str, rect: pygame.Rect, active: bool):
    pygame.draw.rect(screen, (15, 15, 15), rect, border_radius=8)
    pygame.draw.rect(screen, (125, 220, 130) if active else (240, 240, 240), rect, width=2, border_radius=8)
    screen.blit(font.render(label, True, (240, 240, 240)), (rect.x, rect.y - 24))
    screen.blit(font.render(value if value else "_", True, (240, 240, 240)), (rect.x + 8, rect.y + 8))


def _make_tone(freq: float, duration_ms: int, volume: float = 0.3) -> pygame.mixer.Sound:
    sample_rate = 22050
    sample_count = int(sample_rate * duration_ms / 1000)
    amplitude = int(32767 * max(0.0, min(volume, 1.0)))
    samples = array(
        "h",
        [int(amplitude * math.sin(2.0 * math.pi * freq * i / sample_rate)) for i in range(sample_count)],
    )
    return pygame.mixer.Sound(buffer=samples.tobytes())


def build_sounds() -> dict[str, pygame.mixer.Sound]:
    return {
        "click": _make_tone(640, 70, 0.18),
        "food": _make_tone(820, 80, 0.22),
        "poison": _make_tone(210, 140, 0.26),
        "power_up": _make_tone(980, 120, 0.25),
        "shield_block": _make_tone(560, 120, 0.22),
        "level_up": _make_tone(1100, 150, 0.25),
        "game_over": _make_tone(170, 300, 0.3),
    }


def play_sound(settings: dict, sounds: dict[str, pygame.mixer.Sound], name: str) -> None:
    if settings.get("sound") and name in sounds:
        sounds[name].play()


def run() -> None:
    pygame.init()
    pygame.font.init()
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=1)
        sounds = build_sounds()
    except pygame.error:
        sounds = {}
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("TSIS4 Snake")
    clock = pygame.time.Clock()
    fonts = {
        "title": pygame.font.SysFont("arial", 40, bold=True),
        "normal": pygame.font.SysFont("arial", 26),
        "small": pygame.font.SysFont("arial", 22),
    }

    settings = load_settings(SETTINGS_PATH)
    game = SnakeGame(settings)
    state = "menu"
    username = ""
    username_focus = True
    game_saved = False
    try:
        db = Database(DB_CONFIG)
    except Exception as exc:  # noqa: BLE001
        pygame.quit()
        print("Database connection failed. Start PostgreSQL in Docker and run again.")
        print(f"Reason: {exc}")
        return

    leaderboard_rows = []
    last_result = {"score": 0, "level": 1}

    running = True
    while running:
        dt_ms = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "menu":
                buttons = {
                    "play": Button(pygame.Rect(300, 200, 200, 50), "Play"),
                    "leaderboard": Button(pygame.Rect(300, 265, 200, 50), "Leaderboard"),
                    "settings": Button(pygame.Rect(300, 330, 200, 50), "Settings"),
                    "quit": Button(pygame.Rect(300, 395, 200, 50), "Quit"),
                }
                if buttons["play"].clicked(event) and username.strip():
                    play_sound(settings, sounds, "click")
                    game = SnakeGame(settings)
                    game.set_personal_best(db.get_personal_best(username.strip()))
                    state = "game"
                    game_saved = False
                elif buttons["leaderboard"].clicked(event):
                    play_sound(settings, sounds, "click")
                    leaderboard_rows = db.get_top10()
                    state = "leaderboard"
                elif buttons["settings"].clicked(event):
                    play_sound(settings, sounds, "click")
                    state = "settings"
                elif buttons["quit"].clicked(event):
                    play_sound(settings, sounds, "click")
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    username_focus = pygame.Rect(255, 130, 290, 45).collidepoint(event.pos)

                if event.type == pygame.KEYDOWN and username_focus:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN and username.strip():
                        play_sound(settings, sounds, "click")
                        game = SnakeGame(settings)
                        game.set_personal_best(db.get_personal_best(username.strip()))
                        state = "game"
                        game_saved = False
                    elif event.unicode.isprintable() and len(username) < 18:
                        username += event.unicode

            elif state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        game.set_direction((0, -1))
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        game.set_direction((0, 1))
                    elif event.key in (pygame.K_a, pygame.K_LEFT):
                        game.set_direction((-1, 0))
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        game.set_direction((1, 0))
                    elif event.key == pygame.K_ESCAPE:
                        state = "menu"

            elif state == "game_over":
                retry_btn = Button(pygame.Rect(260, 390, 120, 52), "Retry")
                menu_btn = Button(pygame.Rect(410, 390, 150, 52), "Main Menu")
                if retry_btn.clicked(event):
                    play_sound(settings, sounds, "click")
                    game = SnakeGame(settings)
                    game.set_personal_best(db.get_personal_best(username.strip()))
                    game_saved = False
                    state = "game"
                elif menu_btn.clicked(event):
                    play_sound(settings, sounds, "click")
                    state = "menu"

            elif state == "leaderboard":
                back_btn = Button(pygame.Rect(30, 24, 120, 45), "Back")
                if back_btn.clicked(event):
                    play_sound(settings, sounds, "click")
                    state = "menu"

            elif state == "settings":
                back_btn = Button(pygame.Rect(30, 24, 170, 45), "Save & Back")
                grid_btn = Button(pygame.Rect(250, 170, 300, 50), "Toggle Grid")
                sound_btn = Button(pygame.Rect(250, 240, 300, 50), "Toggle Sound")
                if back_btn.clicked(event):
                    play_sound(settings, sounds, "click")
                    save_settings(SETTINGS_PATH, settings)
                    state = "menu"
                if grid_btn.clicked(event):
                    play_sound(settings, sounds, "click")
                    settings["grid"] = not settings["grid"]
                if sound_btn.clicked(event):
                    settings["sound"] = not settings["sound"]
                    play_sound(settings, sounds, "click")
                for idx, (name, color) in enumerate(SNAKE_COLORS.items()):
                    btn = Button(pygame.Rect(250, 320 + idx * 60, 220, 48), name)
                    if btn.clicked(event):
                        play_sound(settings, sounds, "click")
                        settings["snake_color"] = color[:]

        screen.fill((22, 22, 22))
        if state == "menu":
            screen.blit(fonts["title"].render("TSIS4 Snake", True, (245, 245, 245)), (280, 55))
            draw_input(screen, fonts["small"], "Username", username, pygame.Rect(255, 130, 290, 45), username_focus)
            pb = db.get_personal_best(username.strip()) if username.strip() else 0
            screen.blit(fonts["small"].render(f"Personal best: {pb}", True, (240, 240, 240)), (255, 182))

            for b in [
                Button(pygame.Rect(300, 200, 200, 50), "Play"),
                Button(pygame.Rect(300, 265, 200, 50), "Leaderboard"),
                Button(pygame.Rect(300, 330, 200, 50), "Settings"),
                Button(pygame.Rect(300, 395, 200, 50), "Quit"),
            ]:
                b.draw(screen, fonts["normal"])

        elif state == "game":
            game.draw(screen, fonts, settings)
            game.update(dt_ms)
            while game.sfx_events:
                play_sound(settings, sounds, game.sfx_events.pop(0))
            if game.game_over:
                last_result = {"score": game.score, "level": game.level}
                if not game_saved and username.strip():
                    db.save_session(username.strip(), game.score, game.level)
                    game_saved = True
                    game.personal_best = max(game.personal_best, game.score)
                state = "game_over"

        elif state == "game_over":
            screen.blit(fonts["title"].render("Game Over", True, (245, 245, 245)), (290, 140))
            lines = [
                f"Final score: {last_result['score']}",
                f"Level reached: {last_result['level']}",
                f"Personal best: {game.personal_best}",
                f"Reason: {game.fail_reason}",
            ]
            for idx, line in enumerate(lines):
                screen.blit(fonts["normal"].render(line, True, (240, 240, 240)), (215, 220 + idx * 38))
            Button(pygame.Rect(260, 390, 120, 52), "Retry").draw(screen, fonts["small"])
            Button(pygame.Rect(410, 390, 150, 52), "Main Menu").draw(screen, fonts["small"])

        elif state == "leaderboard":
            screen.blit(fonts["title"].render("Top 10 Leaderboard", True, (245, 245, 245)), (200, 35))
            header = fonts["small"].render("Rank Username         Score  Level  Date", True, (235, 235, 235))
            screen.blit(header, (110, 110))
            for i in range(10):
                if i < len(leaderboard_rows):
                    row = leaderboard_rows[i]
                    date_text = row.played_at.strftime("%Y-%m-%d")
                    uname = row.username
                    score = row.score
                    lvl = row.level_reached
                    text = f"{i + 1:>2}   {uname[:12]:<12}   {score:>4}    {lvl:>2}    {date_text}"
                else:
                    text = f"{i + 1:>2}   {'---':<12}   {0:>4}    {0:>2}    {'-':<10}"
                screen.blit(fonts["small"].render(text, True, (240, 240, 240)), (110, 155 + i * 40))
            Button(pygame.Rect(30, 24, 120, 45), "Back").draw(screen, fonts["small"])

        elif state == "settings":
            screen.blit(fonts["title"].render("Settings", True, (245, 245, 245)), (325, 80))
            Button(pygame.Rect(30, 24, 170, 45), "Save & Back").draw(screen, fonts["small"])
            Button(pygame.Rect(250, 170, 300, 50), "Toggle Grid").draw(screen, fonts["small"], active=settings["grid"])
            Button(pygame.Rect(250, 240, 300, 50), "Toggle Sound").draw(screen, fonts["small"], active=settings["sound"])
            screen.blit(fonts["small"].render(f"Grid: {'ON' if settings['grid'] else 'OFF'}", True, (235, 235, 235)), (570, 180))
            screen.blit(fonts["small"].render(f"Sound: {'ON' if settings['sound'] else 'OFF'}", True, (235, 235, 235)), (555, 250))
            screen.blit(fonts["normal"].render("Snake color:", True, (240, 240, 240)), (250, 300))
            for idx, (name, color) in enumerate(SNAKE_COLORS.items()):
                active = settings["snake_color"] == color
                Button(pygame.Rect(250, 320 + idx * 60, 220, 48), name).draw(screen, fonts["small"], active=active)
                pygame.draw.rect(screen, tuple(color), (485, 332 + idx * 60, 32, 24), border_radius=4)

        pygame.display.flip()

    save_settings(SETTINGS_PATH, settings)
    pygame.quit()


if __name__ == "__main__":
    run()
