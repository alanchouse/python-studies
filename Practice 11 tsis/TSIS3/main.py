from pathlib import Path
from array import array
import math

import pygame

from persistence import (
    load_leaderboard,
    load_settings,
    save_leaderboard,
    save_settings,
)
from racer import CAR_COLORS, FINISH_DISTANCE, GameSession, HEIGHT, WIDTH
from ui import Button, draw_input_box, draw_panel, draw_title


BASE_DIR = Path(__file__).resolve().parent
SETTINGS_PATH = BASE_DIR / "settings.json"
LEADERBOARD_PATH = BASE_DIR / "leaderboard.json"


def _make_tone(freq: float, duration_ms: int, volume: float = 0.28) -> pygame.mixer.Sound:
    sample_rate = 22050
    sample_count = int(sample_rate * duration_ms / 1000)
    amplitude = int(32767 * max(0.0, min(volume, 1.0)))
    samples = array(
        "h",
        [int(amplitude * math.sin(2.0 * math.pi * freq * i / sample_rate)) for i in range(sample_count)],
    )
    return pygame.mixer.Sound(buffer=samples.tobytes())


def _build_sounds() -> dict[str, pygame.mixer.Sound]:
    return {
        "click": _make_tone(620, 65, 0.18),
        "coin": _make_tone(900, 75, 0.22),
        "powerup": _make_tone(1100, 110, 0.22),
        "nitro": _make_tone(800, 120, 0.23),
        "bump": _make_tone(220, 120, 0.22),
        "shield": _make_tone(520, 130, 0.2),
        "crash": _make_tone(170, 180, 0.28),
        "game_over": _make_tone(150, 320, 0.3),
        "finished": _make_tone(1200, 240, 0.22),
    }


def _play_sound(settings: dict, sounds: dict[str, pygame.mixer.Sound], key: str) -> None:
    if settings.get("sound") and key in sounds:
        sounds[key].play()


def main() -> None:
    pygame.init()
    pygame.font.init()
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=1)
        sounds = _build_sounds()
    except pygame.error:
        sounds = {}
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS3 Racer")
    clock = pygame.time.Clock()
    fonts = {
        "title": pygame.font.SysFont("arial", 44, bold=True),
        "menu": pygame.font.SysFont("arial", 30, bold=True),
        "normal": pygame.font.SysFont("arial", 24),
        "small": pygame.font.SysFont("arial", 22),
    }

    settings = load_settings(SETTINGS_PATH)
    leaderboard = load_leaderboard(LEADERBOARD_PATH)
    session = GameSession(settings)

    state = "menu"
    username = ""
    username_focus = True
    leaderboard_tab = "global"
    game_result = "dead"
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "menu":
                menu_buttons = _menu_buttons()
                if menu_buttons["play"].clicked(event) and username.strip():
                    _play_sound(settings, sounds, "click")
                    session = GameSession(settings)
                    state = "game"
                elif menu_buttons["leaderboard"].clicked(event):
                    _play_sound(settings, sounds, "click")
                    state = "leaderboard"
                elif menu_buttons["settings"].clicked(event):
                    _play_sound(settings, sounds, "click")
                    state = "settings"
                elif menu_buttons["quit"].clicked(event):
                    _play_sound(settings, sounds, "click")
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    username_focus = pygame.Rect(105, 180, 310, 48).collidepoint(event.pos)
                if event.type == pygame.KEYDOWN and username_focus:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN and username.strip():
                        _play_sound(settings, sounds, "click")
                        session = GameSession(settings)
                        state = "game"
                    elif event.unicode.isprintable() and len(username) < 18:
                        username += event.unicode

            elif state == "settings":
                settings_buttons = _settings_buttons()
                if settings_buttons["back"].clicked(event):
                    _play_sound(settings, sounds, "click")
                    save_settings(SETTINGS_PATH, settings)
                    state = "menu"
                if settings_buttons["sound"].clicked(event):
                    settings["sound"] = not settings["sound"]
                    _play_sound(settings, sounds, "click")
                for color in CAR_COLORS:
                    if settings_buttons[f"color:{color}"].clicked(event):
                        _play_sound(settings, sounds, "click")
                        settings["car_color"] = color
                for difficulty in ["easy", "normal", "hard"]:
                    if settings_buttons[f"difficulty:{difficulty}"].clicked(event):
                        _play_sound(settings, sounds, "click")
                        settings["difficulty"] = difficulty
                session.settings = settings

            elif state == "leaderboard":
                tab_buttons = _leaderboard_tab_buttons()
                if tab_buttons["global"].clicked(event):
                    _play_sound(settings, sounds, "click")
                    leaderboard_tab = "global"
                elif tab_buttons["my"].clicked(event):
                    _play_sound(settings, sounds, "click")
                    leaderboard_tab = "my"
                if _back_button().clicked(event):
                    _play_sound(settings, sounds, "click")
                    state = "menu"

            elif state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        session.try_move(-1)
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        session.try_move(1)
                    elif event.key == pygame.K_ESCAPE:
                        state = "menu"

            elif state == "game_over":
                over_buttons = _game_over_buttons()
                if over_buttons["retry"].clicked(event):
                    _play_sound(settings, sounds, "click")
                    session = GameSession(settings)
                    state = "game"
                elif over_buttons["menu"].clicked(event):
                    _play_sound(settings, sounds, "click")
                    state = "menu"

        screen.fill((26, 26, 26))
        if state == "menu":
            _draw_menu(screen, fonts, username, username_focus)
        elif state == "settings":
            _draw_settings(screen, fonts, settings)
        elif state == "leaderboard":
            _draw_leaderboard(screen, fonts, leaderboard, username, leaderboard_tab)
        elif state == "game":
            result = session.step(dt)
            while session.sfx_events:
                _play_sound(settings, sounds, session.sfx_events.pop(0))
            session.draw(screen, fonts)
            if result in ("dead", "finished"):
                _play_sound(settings, sounds, "finished" if result == "finished" else "game_over")
                game_result = result
                new_row = {
                    "name": username,
                    "score": session.score + (120 if result == "finished" else 0),
                    "distance": int(min(session.distance, FINISH_DISTANCE)),
                    "coins": session.coins,
                }
                leaderboard.append(new_row)
                leaderboard = sorted(leaderboard, key=lambda row: row["score"], reverse=True)[:10]
                save_leaderboard(LEADERBOARD_PATH, leaderboard)
                state = "game_over"
        elif state == "game_over":
            _draw_game_over(screen, fonts, session, game_result)

        pygame.display.flip()

    save_settings(SETTINGS_PATH, settings)
    pygame.quit()


def _menu_buttons() -> dict[str, Button]:
    return {
        "play": Button(pygame.Rect(180, 280, 160, 55), "Play"),
        "leaderboard": Button(pygame.Rect(145, 355, 230, 55), "Leaderboard"),
        "settings": Button(pygame.Rect(170, 430, 180, 55), "Settings"),
        "quit": Button(pygame.Rect(185, 505, 150, 55), "Quit"),
    }


def _settings_buttons() -> dict[str, Button]:
    buttons = {
        "sound": Button(pygame.Rect(95, 190, 330, 50), "Toggle Sound"),
        "back": Button(pygame.Rect(190, 680, 140, 50), "Back"),
    }
    for idx, color in enumerate(CAR_COLORS):
        buttons[f"color:{color}"] = Button(pygame.Rect(60 + idx * 115, 315, 100, 48), color.title())
    for idx, difficulty in enumerate(["easy", "normal", "hard"]):
        buttons[f"difficulty:{difficulty}"] = Button(
            pygame.Rect(70 + idx * 150, 470, 130, 48),
            difficulty.title(),
        )
    return buttons


def _leaderboard_tab_buttons() -> dict[str, Button]:
    return {
        "global": Button(pygame.Rect(138, 160, 118, 42), "Global"),
        "my": Button(pygame.Rect(270, 160, 118, 42), "My Best"),
    }


def _game_over_buttons() -> dict[str, Button]:
    return {
        "retry": Button(pygame.Rect(135, 510, 110, 52), "Retry"),
        "menu": Button(pygame.Rect(275, 510, 110, 52), "Main Menu"),
    }


def _back_button() -> Button:
    return Button(pygame.Rect(20, 20, 100, 45), "Back")


def _draw_menu(
    screen: pygame.Surface,
    fonts: dict[str, pygame.font.Font],
    username: str,
    username_focus: bool,
) -> None:
    draw_title(screen, fonts["title"], "TSIS3 RACER")
    panel = pygame.Rect(90, 150, 340, 430)
    draw_panel(screen, panel)
    draw_input_box(
        screen,
        fonts["normal"],
        "Username",
        username,
        pygame.Rect(105, 180, 310, 48),
        username_focus,
    )
    hint = fonts["small"].render("Type name and press Enter or Play", True, (240, 240, 240))
    screen.blit(hint, (108, 242))
    for button in _menu_buttons().values():
        button.draw(screen, fonts["menu"])


def _draw_settings(screen: pygame.Surface, fonts: dict[str, pygame.font.Font], settings: dict) -> None:
    draw_title(screen, fonts["title"], "Settings")
    panel = pygame.Rect(35, 120, 450, 620)
    draw_panel(screen, panel)
    buttons = _settings_buttons()
    buttons["sound"].draw(screen, fonts["normal"], active=settings["sound"])
    sound_txt = fonts["small"].render(f"Sound: {'ON' if settings['sound'] else 'OFF'}", True, (250, 250, 250))
    screen.blit(sound_txt, (170, 252))

    color_txt = fonts["normal"].render("Car color:", True, (250, 250, 250))
    screen.blit(color_txt, (55, 282))
    for color in CAR_COLORS:
        buttons[f"color:{color}"].draw(screen, fonts["small"], active=settings["car_color"] == color)

    diff_txt = fonts["normal"].render("Difficulty:", True, (250, 250, 250))
    screen.blit(diff_txt, (55, 438))
    for difficulty in ["easy", "normal", "hard"]:
        buttons[f"difficulty:{difficulty}"].draw(
            screen,
            fonts["small"],
            active=settings["difficulty"] == difficulty,
        )
    buttons["back"].draw(screen, fonts["normal"])


def _draw_leaderboard(
    screen: pygame.Surface,
    fonts: dict[str, pygame.font.Font],
    leaderboard: list[dict],
    username: str,
    tab: str,
) -> None:
    draw_title(screen, fonts["title"], "Top 10")
    panel = pygame.Rect(35, 120, 450, 620)
    draw_panel(screen, panel)
    tab_buttons = _leaderboard_tab_buttons()
    tab_buttons["global"].draw(screen, fonts["small"], active=tab == "global")
    tab_buttons["my"].draw(screen, fonts["small"], active=tab == "my")
    title = fonts["small"].render("Rank   Name           Score   Dist   Coins", True, (240, 240, 240))
    screen.blit(title, (60, 220))
    rows = leaderboard
    if tab == "my":
        rows = [row for row in leaderboard if row["name"] == username]
    for idx in range(10):
        row = rows[idx] if idx < len(rows) else None
        if row:
            text = f"{idx + 1:>2}     {row['name'][:12]:<12}  {row['score']:>5}   {row['distance']:>4}   {row['coins']:>3}"
        else:
            text = f"{idx + 1:>2}     {'---':<12}  {'0':>5}   {'0':>4}   {'0':>3}"
        line = fonts["small"].render(text, True, (250, 250, 250))
        screen.blit(line, (60, 260 + idx * 38))
    if tab == "my" and not rows:
        note = fonts["small"].render("No personal result yet.", True, (220, 220, 220))
        screen.blit(note, (145, 650))
    _back_button().draw(screen, fonts["normal"])


def _draw_game_over(
    screen: pygame.Surface,
    fonts: dict[str, pygame.font.Font],
    session: GameSession,
    game_result: str,
) -> None:
    draw_title(screen, fonts["title"], "FINISH!" if game_result == "finished" else "GAME OVER")
    panel = pygame.Rect(75, 175, 370, 410)
    draw_panel(screen, panel)

    lines = [
        f"Score: {session.score + (120 if game_result == 'finished' else 0)}",
        f"Distance: {int(min(session.distance, FINISH_DISTANCE))}",
        f"Coins: {session.coins}",
        f"Status: {'Track completed' if game_result == 'finished' else 'Crash limit reached'}",
    ]
    for i, line in enumerate(lines):
        txt = fonts["normal"].render(line, True, (245, 245, 245))
        screen.blit(txt, (120, 255 + i * 56))
    for button in _game_over_buttons().values():
        button.draw(screen, fonts["normal"])


if __name__ == "__main__":
    main()
