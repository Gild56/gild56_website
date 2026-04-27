from src.logic.data_loader import load_file
import threading
from functools import lru_cache
import time


@lru_cache
def get_players() -> list[tuple[str, list[str], list[str], list[str], list[str], list[str]]]:
    players = load_file("players")

    levels_list = load_file("levels_list")
    challenges_list = load_file("challenges_list")
    server_levels_list = load_file("server_levels_list")
    server_challenges_list = load_file("server_challenges_list")

    updated_players: list[tuple[str, list[str], list[str], list[str], list[str], list[str]]] = []

    for name, info in players:

        # Gild List
        if name == "Gild56":
            passed_levels = [
                level[0] for level in levels_list if level[3] != ""
            ]
        else:
            passed_levels = [
                level[0] for level in levels_list if name in level[4]
            ]

        # Gild Challenges List
        if name == "Gild56":
            passed_challenges = [
                challenge[0] for challenge in challenges_list if challenge[3] != ""
            ]
        else:
            passed_challenges = [
                challenge[0] for challenge in challenges_list if name in challenge[4]
            ]

        # Gild Server List
        if name == "Gild56":
            passed_server_levels = [
                level[0] for level in server_levels_list if level[3] != ""
            ]
        else:
            passed_server_levels = [
                level[0] for level in server_levels_list if name in level[4]
            ]

        # Gild Server Challenges List
        if name == "Gild56":
            passed_server_challenges = [
                challenge[0] for challenge in server_challenges_list if challenge[3] != ""
            ]
        else:
            passed_server_challenges = [
                challenge[0] for challenge in server_challenges_list if name in challenge[4]
            ]

        updated_players.append((name, info, passed_levels, passed_challenges, passed_server_levels, passed_server_challenges))

    return updated_players


def clear_cache():
    while True:
        time.sleep(24 * 60 * 60)  # 24h

        get_players.cache_clear()

threading.Thread(
    target=clear_cache,
    daemon=True
).start()
