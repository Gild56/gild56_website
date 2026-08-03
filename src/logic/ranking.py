from src.logic.players import get_players
from src.logic.data_loader import load_file
import threading
from functools import lru_cache
import time
import math

@lru_cache
def get_points_by_place(rank: int) -> float:
    if rank < 1:
        return 0

    if rank <= 8:
        return 1000 - (rank - 1) * 40

    if rank <= 20:
        return 660 - (rank - 9) * 20

    if rank <= 50:
        return 396 - (rank - 21) * 4

    if rank <= 75:
        return 272 - (rank - 51) * 8

    if rank <= 150:
        return 80 - (rank - 75)

    if rank <= 250:
        return 4.6 - ((rank - 151) // 10) * 0.4

    level = math.ceil((rank - 250) / 95)
    return max(1.00 - level * 0.01, 0.05)


@lru_cache
def get_top_players(type: str | None = "levels_list") -> list[tuple[str, list[str], list[str], list[str], list[str], list[str], int]]:
    top = load_file(type)
    players = get_players()

    points = {
        level[0]: get_points_by_place(i + 1)
        for i, level in enumerate(top)
    }

    top_players: list[tuple[str, list[str], list[str], list[str], list[str], list[str], int]] = []

    for name, tag, passed_levels, passed_challenges, passed_server_levels, passed_server_challenges in players:
        if type == "levels_list":
            total_points = sum(points.get(lvl, 0) for lvl in passed_levels)
        elif type == "challenges_list":
            total_points = sum(points.get(lvl, 0) for lvl in passed_challenges)
        elif type == "server_levels_list":
            total_points = sum(points.get(lvl, 0) for lvl in passed_server_levels)
        else:  # elif type == "server_challenges_list":
            total_points = sum(points.get(lvl, 0) for lvl in passed_server_challenges)

        top_players.append(
            (name, tag, passed_levels, passed_challenges, passed_server_levels, passed_server_challenges, total_points)
        )

    top_players.sort(key=lambda x: x[6], reverse=True)

    return top_players


def clear_cache():
    while True:
        time.sleep(24 * 60 * 60)  # 24h

        get_top_players.cache_clear()

threading.Thread(
    target=clear_cache,
    daemon=True
).start()
