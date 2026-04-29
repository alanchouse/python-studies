from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor


@dataclass
class LeaderboardRow:
    username: str
    score: int
    level_reached: int
    played_at: datetime


class Database:
    def __init__(self, config: dict):
        self.config = config
        self._init_schema()

    def _connect(self):
        return psycopg2.connect(**self.config)

    def _init_schema(self) -> None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS players (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL
                    );
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS game_sessions (
                        id SERIAL PRIMARY KEY,
                        player_id INTEGER REFERENCES players(id),
                        score INTEGER NOT NULL,
                        level_reached INTEGER NOT NULL,
                        played_at TIMESTAMP DEFAULT NOW()
                    );
                    """
                )
            conn.commit()

    def _get_or_create_player_id(self, username: str) -> int:
        clean = username.strip()[:50]
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO players (username)
                    VALUES (%s)
                    ON CONFLICT (username) DO UPDATE SET username = EXCLUDED.username
                    RETURNING id;
                    """,
                    (clean,),
                )
                player_id = cur.fetchone()[0]
            conn.commit()
        return player_id

    def save_session(self, username: str, score: int, level_reached: int) -> None:
        player_id = self._get_or_create_player_id(username)
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO game_sessions (player_id, score, level_reached)
                    VALUES (%s, %s, %s);
                    """,
                    (player_id, score, level_reached),
                )
            conn.commit()

    def get_top10(self) -> list[LeaderboardRow]:
        with self._connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT p.username, g.score, g.level_reached, g.played_at
                    FROM game_sessions g
                    JOIN players p ON p.id = g.player_id
                    ORDER BY g.score DESC, g.played_at ASC
                    LIMIT 10;
                    """
                )
                rows = cur.fetchall()
        return [LeaderboardRow(**row) for row in rows]

    def get_personal_best(self, username: str) -> int:
        clean = username.strip()[:50]
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT COALESCE(MAX(g.score), 0)
                    FROM game_sessions g
                    JOIN players p ON p.id = g.player_id
                    WHERE p.username = %s;
                    """,
                    (clean,),
                )
                best = cur.fetchone()[0]
        return int(best or 0)
