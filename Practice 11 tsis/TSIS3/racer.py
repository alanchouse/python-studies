import random
from dataclasses import dataclass

import pygame

from persistence import DIFFICULTY_FACTORS


WIDTH, HEIGHT = 520, 780
ROAD_MARGIN = 70
LANE_COUNT = 3
LANE_WIDTH = (WIDTH - ROAD_MARGIN * 2) // LANE_COUNT
FINISH_DISTANCE = 3000

CAR_COLORS = {
    "red": (220, 70, 70),
    "blue": (70, 140, 240),
    "green": (75, 185, 90),
    "yellow": (230, 205, 80),
}

COIN_VALUES = [1, 2, 5]


@dataclass
class SpawnedObject:
    lane: int
    y: float
    kind: str
    speed_mul: float = 1.0
    value: int = 0
    timer: float = 0.0
    width: int = LANE_WIDTH - 24
    height: int = 44
    hp: int = 1

    def rect(self) -> pygame.Rect:
        x = ROAD_MARGIN + self.lane * LANE_WIDTH + (LANE_WIDTH - self.width) // 2
        return pygame.Rect(int(x), int(self.y), self.width, self.height)


class GameSession:
    def __init__(self, settings: dict):
        self.settings = settings
        self.reset()

    def reset(self) -> None:
        self.player_lane = 1
        self.target_lane = 1
        self.player_y = HEIGHT - 120
        self.player_x = self._lane_x(self.player_lane)
        self.scroll_y = 0.0
        self.base_speed = 270.0
        self.distance = 0.0
        self.coins = 0
        self.score = 0
        self.crashes_left = 1
        self.shield_ready = False
        self.active_power = None
        self.power_time = 0.0
        self.finished = False
        self.hit_flash = 0.0
        self.traffic: list[SpawnedObject] = []
        self.obstacles: list[SpawnedObject] = []
        self.coins_items: list[SpawnedObject] = []
        self.powerups: list[SpawnedObject] = []
        self.events: list[SpawnedObject] = []
        self.spawn_timers = {
            "traffic": 0.0,
            "obstacle": 0.0,
            "coin": 0.0,
            "powerup": 2.0,
            "event": 1.5,
        }
        self.sfx_events: list[str] = []

    @property
    def speed_factor(self) -> float:
        distance_scale = 1.0 + min(self.distance / 3000.0, 0.9)
        return DIFFICULTY_FACTORS[self.settings["difficulty"]] * distance_scale

    @property
    def speed(self) -> float:
        boost = 1.5 if self.active_power == "nitro" else 1.0
        return self.base_speed * self.speed_factor * boost

    def _lane_x(self, lane: int) -> float:
        return float(ROAD_MARGIN + lane * LANE_WIDTH + 10)

    def player_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.player_x), int(self.player_y), LANE_WIDTH - 20, 72)

    def try_move(self, direction: int) -> None:
        if direction < 0:
            self.target_lane = max(0, self.target_lane - 1)
        elif direction > 0:
            self.target_lane = min(LANE_COUNT - 1, self.target_lane + 1)

    def step(self, dt: float) -> str:
        if self.finished:
            return "finished"
        target_x = self._lane_x(self.target_lane)
        move_speed = 470.0
        if self.player_x < target_x:
            self.player_x = min(target_x, self.player_x + move_speed * dt)
        elif self.player_x > target_x:
            self.player_x = max(target_x, self.player_x - move_speed * dt)
        self.player_lane = int(round((self.player_x - ROAD_MARGIN - 10) / LANE_WIDTH))
        self.player_lane = max(0, min(LANE_COUNT - 1, self.player_lane))

        self.distance += self.speed * dt * 0.06
        self.scroll_y += self.speed * dt
        self.score = int(self.coins * 15 + self.distance * 2)

        if self.active_power == "nitro":
            self.power_time -= dt
            if self.power_time <= 0:
                self.active_power = None
        self.hit_flash = max(0.0, self.hit_flash - dt)

        self._spawn(dt)
        self._move_entities(dt)
        result = self._handle_collisions()
        if self.distance >= FINISH_DISTANCE:
            self.finished = True
            return "finished"
        return result

    def _spawn(self, dt: float) -> None:
        traffic_interval = max(0.32, 1.2 / self.speed_factor)
        obstacle_interval = max(0.45, 1.8 / self.speed_factor)
        coin_interval = 0.45
        power_interval = 5.5
        event_interval = max(2.6, 6.0 / self.speed_factor)

        self.spawn_timers["traffic"] += dt
        self.spawn_timers["obstacle"] += dt
        self.spawn_timers["coin"] += dt
        self.spawn_timers["powerup"] += dt
        self.spawn_timers["event"] += dt

        if self.spawn_timers["traffic"] >= traffic_interval:
            self.spawn_timers["traffic"] = 0.0
            lane = self._safe_lane()
            self.traffic.append(
                SpawnedObject(lane=lane, y=-90, kind="traffic", speed_mul=random.uniform(0.75, 1.1), height=70)
            )
        if self.spawn_timers["obstacle"] >= obstacle_interval:
            self.spawn_timers["obstacle"] = 0.0
            lane = self._safe_lane()
            kind = random.choice(["barrier", "oil", "pothole"])
            speed_mul = 1.0 if kind != "barrier" else 0.9
            self.obstacles.append(SpawnedObject(lane=lane, y=-70, kind=kind, speed_mul=speed_mul, height=48))
        if self.spawn_timers["coin"] >= coin_interval:
            self.spawn_timers["coin"] = 0.0
            lane = random.randrange(0, LANE_COUNT)
            value = random.choices(COIN_VALUES, weights=[70, 22, 8], k=1)[0]
            self.coins_items.append(SpawnedObject(lane=lane, y=-40, kind="coin", value=value, width=26, height=26))
        if self.spawn_timers["powerup"] >= power_interval:
            self.spawn_timers["powerup"] = 0.0
            lane = self._safe_lane()
            kind = random.choice(["nitro", "shield", "repair"])
            self.powerups.append(
                SpawnedObject(lane=lane, y=-45, kind=kind, width=32, height=32, timer=7.0)
            )
        if self.spawn_timers["event"] >= event_interval:
            self.spawn_timers["event"] = 0.0
            kind = random.choice(["moving_barrier", "speed_bump", "nitro_strip"])
            if kind == "moving_barrier":
                lane = random.randrange(0, LANE_COUNT)
                self.events.append(SpawnedObject(lane=lane, y=-80, kind=kind, height=38, hp=1))
            else:
                lane = random.randrange(0, LANE_COUNT)
                self.events.append(SpawnedObject(lane=lane, y=-100, kind=kind, height=60))

    def _move_entities(self, dt: float) -> None:
        for obj in self.traffic + self.obstacles + self.coins_items + self.powerups + self.events:
            obj.y += self.speed * dt * obj.speed_mul
        for power in self.powerups:
            power.timer -= dt
        self.traffic = [o for o in self.traffic if o.y < HEIGHT + 90]
        self.obstacles = [o for o in self.obstacles if o.y < HEIGHT + 90]
        self.coins_items = [o for o in self.coins_items if o.y < HEIGHT + 45]
        self.powerups = [o for o in self.powerups if o.y < HEIGHT + 45 and o.timer > 0]
        self.events = [o for o in self.events if o.y < HEIGHT + 120]
        for event in self.events:
            if event.kind == "moving_barrier" and random.random() < 0.02:
                event.lane = max(0, min(LANE_COUNT - 1, event.lane + random.choice([-1, 1])))

    def _handle_collisions(self) -> str:
        player = self.player_rect()
        for coin in list(self.coins_items):
            if player.colliderect(coin.rect()):
                self.coins += coin.value
                self.coins_items.remove(coin)
                self.sfx_events.append("coin")

        for power in list(self.powerups):
            if player.colliderect(power.rect()):
                self._activate_power(power.kind)
                self.powerups.remove(power)
                self.sfx_events.append("powerup")

        for obj in self.traffic + self.obstacles + self.events:
            if not player.colliderect(obj.rect()):
                continue
            if obj.kind == "nitro_strip":
                self._activate_power("nitro", duration=3.2)
                self.sfx_events.append("nitro")
                continue
            if obj.kind == "speed_bump":
                self.distance = max(0, self.distance - 16)
                self.hit_flash = 0.2
                self.sfx_events.append("bump")
                continue
            if self.shield_ready:
                self.shield_ready = False
                self.hit_flash = 0.3
                self.sfx_events.append("shield")
                return "running"
            if self.crashes_left > 0:
                self.crashes_left -= 1
                self.hit_flash = 0.45
                self.sfx_events.append("crash")
                return "running"
            self.sfx_events.append("game_over")
            return "dead"
        return "running"

    def _safe_lane(self) -> int:
        lanes = [0, 1, 2]
        if random.random() < 0.82:
            lanes = [lane for lane in lanes if lane != self.player_lane]
        if not lanes:
            lanes = [0, 1, 2]
        return random.choice(lanes)

    def _activate_power(self, kind: str, duration: float | None = None) -> None:
        self.active_power = None
        self.power_time = 0.0
        if kind == "shield":
            self.shield_ready = True
            self.active_power = "shield"
            self.power_time = 999.0
        elif kind == "repair":
            self.crashes_left += 1
            self.active_power = "repair"
            self.power_time = 1.0
        elif kind == "nitro":
            self.active_power = "nitro"
            self.power_time = duration if duration is not None else random.uniform(3.0, 5.0)

    def draw(self, surface: pygame.Surface, fonts: dict[str, pygame.font.Font]) -> None:
        surface.fill((18, 120, 28))
        pygame.draw.rect(surface, (54, 54, 54), (ROAD_MARGIN, 0, WIDTH - ROAD_MARGIN * 2, HEIGHT))

        lane_line = (230, 230, 230)
        dash_h = 36
        offset = int(self.scroll_y) % (dash_h * 2)
        for lane in range(1, LANE_COUNT):
            x = ROAD_MARGIN + lane * LANE_WIDTH
            for y in range(-offset, HEIGHT, dash_h * 2):
                pygame.draw.rect(surface, lane_line, (x - 2, y, 4, dash_h))

        for coin in self.coins_items:
            pygame.draw.circle(surface, (240, 206, 38), coin.rect().center, coin.width // 2)
            label = fonts["small"].render(str(coin.value), True, (30, 30, 30))
            surface.blit(label, label.get_rect(center=coin.rect().center))

        colors = {
            "traffic": (215, 130, 70),
            "barrier": (215, 95, 95),
            "oil": (20, 20, 20),
            "pothole": (95, 75, 62),
            "moving_barrier": (195, 45, 45),
            "speed_bump": (235, 175, 60),
            "nitro_strip": (100, 210, 255),
            "nitro": (80, 180, 255),
            "shield": (170, 80, 220),
            "repair": (80, 220, 110),
        }
        for group in [self.traffic, self.obstacles, self.events, self.powerups]:
            for obj in group:
                pygame.draw.rect(surface, colors[obj.kind], obj.rect(), border_radius=6)

        car_color = CAR_COLORS.get(self.settings["car_color"], CAR_COLORS["red"])
        if self.hit_flash > 0:
            car_color = (255, 255, 255)
        pygame.draw.rect(surface, car_color, self.player_rect(), border_radius=10)
        if self.shield_ready:
            pygame.draw.rect(surface, (130, 92, 240), self.player_rect().inflate(8, 8), width=3, border_radius=10)

        text_color = (248, 248, 248)
        lines = [
            f"Coins: {self.coins}",
            f"Score: {self.score}",
            f"Distance: {int(self.distance)} / {FINISH_DISTANCE}",
            f"Left: {max(0, int(FINISH_DISTANCE - self.distance))}",
            f"Difficulty scale: {self.speed_factor:.2f}x",
        ]
        for idx, line in enumerate(lines):
            txt = fonts["small"].render(line, True, text_color)
            surface.blit(txt, (12, 12 + idx * 24))

        power_label = "None"
        if self.active_power == "shield":
            power_label = "Shield (until hit)"
        elif self.active_power == "nitro":
            power_label = f"Nitro ({max(0, self.power_time):.1f}s)"
        elif self.active_power == "repair":
            power_label = "Repair (+1 crash)"
        status = fonts["small"].render(f"Power-up: {power_label}", True, text_color)
        surface.blit(status, (12, 134))
