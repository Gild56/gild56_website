from src.logic.data_loader import load_file
import threading
from functools import lru_cache
from typing import Any
import time
import math


@lru_cache
def get_points_by_place(rank: int) -> float:
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
def get_players() -> list[tuple[str, list[str], list[str], list[str], list[str], list[str]]]:
    players = load_file("players")

    levels_list = load_file("levels_list")
    challenges_list = load_file("challenges_list")
    server_levels_list = load_file("server_levels_list")
    server_challenges_list = load_file("server_challenges_list")

    updated_players: list[tuple[str, list[str], list[str], list[str], list[str], list[str]]] = []

    for name, info in players:

        passed_levels = [
            level[0] for level in levels_list if name in level[3]
        ]

        passed_challenges = [
            challenge[0] for challenge in challenges_list if name in challenge[3]
        ]

        passed_server_levels = [
            level[0] for level in server_levels_list if name in level[3]
        ]

        passed_server_challenges = [
            challenge[0] for challenge in server_challenges_list if name in challenge[3]
        ]

        updated_players.append((name, info, passed_levels, passed_challenges, passed_server_levels, passed_server_challenges))

    return updated_players


@lru_cache
def get_top_players() -> list[tuple[str, list[str], list[str], list[str], list[str], list[str], int]]:
    players = get_players()

    levels_list = load_file("levels_list")
    levels_list_points = {
        level[0]: get_points_by_place(i + 1)
        for i, level in enumerate(levels_list)
    }

    challenges_list = load_file("challenges_list")
    challenges_list_points = {
        level[0]: get_points_by_place(i + 1)
        for i, level in enumerate(challenges_list)
    }

    server_levels_list = load_file("levels_list")
    server_levels_list_points = {
        level[0]: get_points_by_place(i + 1)
        for i, level in enumerate(server_levels_list)
    }

    server_challenges_list = load_file("challenges_list")
    server_challenges_list_points = {
        level[0]: get_points_by_place(i + 1)
        for i, level in enumerate(server_challenges_list)
    }

    top_players: list[tuple[str, list[str], list[str], list[str], list[str], list[str], int]] = []

    for name, tag, passed_levels, passed_challenges, passed_server_levels, passed_server_challenges in players:
        levels_points = sum(levels_list_points.get(lvl, 0) for lvl in passed_levels)
        challenges_points = sum(challenges_list_points.get(lvl, 0) for lvl in passed_challenges)
        server_levels_points = sum(server_levels_list_points.get(lvl, 0) for lvl in passed_server_levels)
        server_challenges_points = sum(server_challenges_list_points.get(lvl, 0) for lvl in passed_server_challenges)

        top_players.append(
            (name, tag, passed_levels, passed_challenges, passed_server_levels, passed_server_challenges, levels_points, challenges_points, server_levels_points, server_challenges_points)
        )

    top_players.sort(key=lambda x: x[6], reverse=True)

    return top_players


@lru_cache
def get_player_ranks() -> dict[str, Any]:
    top_players = get_top_players()

    rank_indexes = {
        "levels_list_place": 6,
        "challenges_list_place": 7,
        "server_levels_list_place": 8,
        "server_challenges_list_place": 9,
    }

    ranks = {}

    for rank_name, points_index in rank_indexes.items():
        sorted_players = sorted(
            top_players,
            key=lambda player: player[points_index],
            reverse=True
        )

        ranks[rank_name] = {
            player[0]: position + 1
            for position, player in enumerate(sorted_players)
        }

    return ranks


def clear_cache():
    while True:
        time.sleep(60 * 10)  # 10 min

        get_players.cache_clear()
        get_top_players.cache_clear()
        get_player_ranks.cache_clear()

threading.Thread(
    target=clear_cache,
    daemon=True
).start()
