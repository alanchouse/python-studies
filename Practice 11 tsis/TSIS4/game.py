from __future__ import annotations

import random
from dataclasses import dataclass

import pygame

from config import GRID_COLS, GRID_ROWS, GRID_SIZE, LEVEL_UP_EVERY


Color = tuple[int, int, int]
Point = tuple[int, int]

FOOD_TYPES = [
    {"points": 1, "color": (90, 210, 90), "ttl_ms": 7000},
    {"points": 2, "color": (80, 170, 255), "ttl_ms": 5500},
    {"points": 3, "color": (255, 210, 90), "ttl_ms": 4200},
]

POWER_UPS = [
    {"kind": "speed", "color": (255, 155, 60), "label": "Speed boost"},
    {"kind": "slow", "color": (140, 180, 255), "label": "Slow motion"},
    {"kind": "shield", "color": (200, 140, 255), "label": "Shield"},
]


@dataclass
class Food:
    position: Point
    points: int
    color: Color
    expires_at: int


@dataclass
class PowerUp:
    kind: str
    label: str
    color: Color
    position: Point
    expires_at: int


class SnakeGame:
    def __init__(self, settings: dict):
        self.settings = settings
        self.reset()

    def reset(self) -> None:
        self.direction = (1, 0)
        self.pending_direction = (1, 0)
        self.snake: list[Point] = [(7, 7), (6, 7), (5, 7)]
        self.score = 0
        self.level = 1
        self.eaten_count = 0
        self.game_over = False
        self.fail_reason = ""
        self.personal_best = 0

        self.shield_ready = False
        self.active_effect: str | None = None
        self.effect_expires_at = 0
        self.power_up: PowerUp | None = None
        self.last_power_spawn_ms = pygame.time.get_ticks()

        self.obstacles: set[Point] = set()
        self.food = self._spawn_food()
        self.poison = self._spawn_poison()
        self.move_buffer_ms = 0
        self.sfx_events: list[str] = []

    def set_personal_best(self, score: int) -> None:
        self.personal_best = score

    def set_direction(self, new_dir: Point) -> None:
        if (new_dir[0] * -1, new_dir[1] * -1) == self.direction:
            return
        self.pending_direction = new_dir

    def _speed_factor(self) -> float:
        factor = 1.0 + (self.level - 1) * 0.12
        if self.active_effect == "speed":
            factor *= 1.6
        elif self.active_effect == "slow":
            factor *= 0.65
        return max(0.3, factor)

    def move_interval_ms(self) -> int:
        return max(45, int(140 / self._speed_factor()))

    def update(self, dt_ms: int) -> None:
        if self.game_over:
            return
        now = pygame.time.get_ticks()

        if self.active_effect in {"speed", "slow"} and now >= self.effect_expires_at:
            self.active_effect = None

        if self.food.expires_at <= now:
            self.food = self._spawn_food()
        if self.power_up and self.power_up.expires_at <= now:
            self.power_up = None

        if self.power_up is None and now - self.last_power_spawn_ms > 9000:
            self.power_up = self._spawn_power_up()
            self.last_power_spawn_ms = now

        self.move_buffer_ms += dt_ms
        interval = self.move_interval_ms()
        while self.move_buffer_ms >= interval and not self.game_over:
            self.move_buffer_ms -= interval
            self._tick_move()

    def _tick_move(self) -> None:
        self.direction = self.pending_direction
        head_x, head_y = self.snake[0]
        nx, ny = head_x + self.direction[0], head_y + self.direction[1]

        collision = self._is_collision((nx, ny))
        if collision:
            if self.shield_ready:
                self.shield_ready = False
                self.fail_reason = "Shield saved you from one collision."
                self.sfx_events.append("shield_block")
                return
            self.game_over = True
            self.fail_reason = collision
            self.sfx_events.append("game_over")
            return

        self.snake.insert(0, (nx, ny))
        ate_growth_food = False

        if (nx, ny) == self.food.position:
            ate_growth_food = True
            self.score += self.food.points
            self.eaten_count += 1
            self.sfx_events.append("food")
            self.food = self._spawn_food()
            if self.eaten_count % LEVEL_UP_EVERY == 0:
                self.level += 1
                self.sfx_events.append("level_up")
                if self.level >= 3:
                    self._generate_obstacles()

        if (nx, ny) == self.poison:
            self.sfx_events.append("poison")
            for _ in range(2):
                if self.snake:
                    self.snake.pop()
            if len(self.snake) <= 1:
                self.game_over = True
                self.fail_reason = "Poison food shortened snake too much."
                self.sfx_events.append("game_over")
                return
            self.poison = self._spawn_poison()

        if self.power_up and (nx, ny) == self.power_up.position:
            self._apply_power_up(self.power_up.kind)
            self.power_up = None
            self.sfx_events.append("power_up")

        if not ate_growth_food:
            self.snake.pop()

    def _apply_power_up(self, kind: str) -> None:
        now = pygame.time.get_ticks()
        if kind == "shield":
            self.shield_ready = True
            self.active_effect = "shield"
            self.effect_expires_at = 0
            return
        self.active_effect = kind
        self.effect_expires_at = now + 5000

    def _is_collision(self, p: Point) -> str | None:
        x, y = p
        if x < 0 or y < 0 or x >= GRID_COLS or y >= GRID_ROWS:
            return "Hit border."
        if p in self.snake:
            return "Hit your body."
        if p in self.obstacles:
            return "Hit an obstacle."
        return None

    def _occupied(self) -> set[Point]:
        occupied = set(self.snake) | set(self.obstacles)
        occupied.add(self.poison if hasattr(self, "poison") else (-1, -1))
        if hasattr(self, "food"):
            occupied.add(self.food.position)
        if self.power_up:
            occupied.add(self.power_up.position)
        return occupied

    def _random_empty_cell(self) -> Point:
        occupied = self._occupied()
        cells = [(x, y) for x in range(GRID_COLS) for y in range(GRID_ROWS) if (x, y) not in occupied]
        return random.choice(cells) if cells else (0, 0)

    def _spawn_food(self) -> Food:
        now = pygame.time.get_ticks()
        food_type = random.choice(FOOD_TYPES)
        return Food(
            position=self._random_empty_cell(),
            points=food_type["points"],
            color=food_type["color"],
            expires_at=now + food_type["ttl_ms"],
        )

    def _spawn_poison(self) -> Point:
        return self._random_empty_cell()

    def _spawn_power_up(self) -> PowerUp:
        now = pygame.time.get_ticks()
        kind = random.choice(POWER_UPS)
        return PowerUp(
            kind=kind["kind"],
            label=kind["label"],
            color=kind["color"],
            position=self._random_empty_cell(),
            expires_at=now + 8000,
        )

    def _generate_obstacles(self) -> None:
        obstacle_count = 10 + self.level * 2
        new_obstacles: set[Point] = set()
        attempts = 0

        while len(new_obstacles) < obstacle_count and attempts < 3000:
            attempts += 1
            px = random.randint(1, GRID_COLS - 2)
            py = random.randint(1, GRID_ROWS - 2)
            candidate = (px, py)
            if candidate in self.snake or candidate == self.food.position or candidate == self.poison:
                continue
            if self.power_up and candidate == self.power_up.position:
                continue
            new_obstacles.add(candidate)

        head = self.snake[0]
        around_head = [
            (head[0] + 1, head[1]),
            (head[0] - 1, head[1]),
            (head[0], head[1] + 1),
            (head[0], head[1] - 1),
        ]
        free_neighbors = [
            p
            for p in around_head
            if 0 <= p[0] < GRID_COLS and 0 <= p[1] < GRID_ROWS and p not in new_obstacles
        ]
        if free_neighbors:
            self.obstacles = new_obstacles

    def draw(self, screen: pygame.Surface, fonts: dict, settings: dict) -> None:
        screen.fill((18, 18, 18))

        if settings["grid"]:
            for x in range(0, GRID_COLS * GRID_SIZE, GRID_SIZE):
                pygame.draw.line(screen, (45, 45, 45), (x, 0), (x, GRID_ROWS * GRID_SIZE))
            for y in range(0, GRID_ROWS * GRID_SIZE, GRID_SIZE):
                pygame.draw.line(screen, (45, 45, 45), (0, y), (GRID_COLS * GRID_SIZE, y))

        for block in self.obstacles:
            pygame.draw.rect(
                screen,
                (95, 95, 95),
                (block[0] * GRID_SIZE, block[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
            )

        pygame.draw.rect(
            screen,
            self.food.color,
            (self.food.position[0] * GRID_SIZE, self.food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
        )
        pygame.draw.rect(
            screen,
            (120, 0, 0),
            (self.poison[0] * GRID_SIZE, self.poison[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
        )

        if self.power_up:
            pygame.draw.rect(
                screen,
                self.power_up.color,
                (
                    self.power_up.position[0] * GRID_SIZE,
                    self.power_up.position[1] * GRID_SIZE,
                    GRID_SIZE,
                    GRID_SIZE,
                ),
            )

        snake_color = tuple(settings["snake_color"])
        for idx, segment in enumerate(self.snake):
            color = (230, 230, 230) if idx == 0 else snake_color
            pygame.draw.rect(
                screen,
                color,
                (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
            )

        y = GRID_ROWS * GRID_SIZE + 4
        if y + 28 > screen.get_height():
            y = screen.get_height() - 28
        status = (
            f"Score: {self.score}   Level: {self.level}   Best: {self.personal_best}   "
            f"Len: {len(self.snake)}   Shield: {'ON' if self.shield_ready else 'OFF'}"
        )
        status_surface = fonts["small"].render(status, True, (245, 245, 245))
        screen.blit(status_surface, (10, y))

        if self.power_up:
            ptxt = fonts["small"].render(f"Power-up on field: {self.power_up.label}", True, (230, 230, 230))
            screen.blit(ptxt, (10, y - 24))
