from src.logic.data_loader import load_file
import threading
from functools import lru_cache
import time


@lru_cache
def get_levels_list() -> list[tuple[str, str, str, str, dict[str, str]]]:
    return load_file("levels_list")


@lru_cache
def get_challenges_list() -> list[tuple[str, str, str, str, dict[str, str]]]:
    return load_file("challenges_list")


@lru_cache
def get_players() -> list[tuple[str, list[str], list[str], list[str]]]:
    players = load_file("players")

    levels_list = get_levels_list()
    challenges_list = get_challenges_list()

    updated_players: list[tuple[str, list[str], list[str], list[str]]] = []

    for name, info in players:
        if name == "Gild56":
            passed_levels_1 = [
                level[0] for level in levels_list if level[3] != ""
            ]
        else:
            passed_levels_1 = [
                level[0] for level in levels_list if name in level[4]
            ]

        if name == "Gild56":
            passed_levels_2 = [
                challenge[0] for challenge in challenges_list if challenge[3] != ""
            ]
        else:
            passed_levels_2 = [
                challenge[0] for challenge in challenges_list if name in challenge[4]
            ]

        updated_players.append((name, info, passed_levels_1, passed_levels_2))

    return updated_players


def clear_cache():
    while True:
        time.sleep(24 * 60 * 60)  # 24h

        get_levels_list.cache_clear()
        get_challenges_list.cache_clear()
        get_players.cache_clear()

threading.Thread(
    target=clear_cache,
    daemon=True
).start()
