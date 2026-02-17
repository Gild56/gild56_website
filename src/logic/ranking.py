from src.logic.players import get_levels_list, get_challenges_list, get_players
import threading
from functools import lru_cache
import time


@lru_cache
def get_points_by_place(rank: int) -> int:
    if rank == 1:
        return 60
    if rank <= 4:
        return 50
    if rank <= 10:
        return 30
    if rank <= 20:
        return 20
    return 10


@lru_cache
def get_top_players() -> list[tuple[str, list[str], list[str], list[str], int]]:
    levels_list_top = get_levels_list()
    players = get_players()

    level_points = {
        level[0]: get_points_by_place(i + 1)
        for i, level in enumerate(levels_list_top)
    }

    top_players: list[tuple[str, list[str], list[str], list[str], int]] = []

    for name, tag, passed_levels_1, passed_levels_2 in players:
        total_points = sum(level_points.get(lvl, 0) for lvl in passed_levels_1)
        top_players.append(
            (name, tag, passed_levels_1, passed_levels_2, total_points)
        )

    top_players.sort(key=lambda x: x[4], reverse=True)

    return top_players


@lru_cache
def get_top_challenge_players() -> list[tuple[str, list[str], list[str], list[str], int]]:
    challenges_list_top = get_challenges_list()
    players = get_players()

    challenge_points = {
        challenge[0]: get_points_by_place(i + 1)
        for i, challenge in enumerate(challenges_list_top)
    }

    top_challenge_players: list[tuple[str, list[str], list[str], list[str], int]] = []

    for name, tag, passed_levels_1, passed_levels_2 in players:
        challenge_score = sum(
            challenge_points.get(lvl, 0) for lvl in passed_levels_2
        )

        top_challenge_players.append(
            (name, tag, passed_levels_1, passed_levels_2, challenge_score)
        )

    top_challenge_players.sort(key=lambda x: x[4], reverse=True)

    return top_challenge_players


def clear_cache():
    while True:
        time.sleep(24 * 60 * 60)  # 24h

        get_top_players.cache_clear()
        get_top_challenge_players.cache_clear()

threading.Thread(
    target=clear_cache,
    daemon=True
).start()
