from typing import Any
from src.logic.data_loader import get_demonlist, load_file
from src.logic.players import get_players
from collections import Counter


def normalize_levels(data: Any) -> list[str]:
    if not data or len(data) < 2:
        return []

    levels_data = data[1]

    if isinstance(levels_data, dict):
        return list(levels_data.keys())

    if isinstance(levels_data, list):
        return levels_data

    return []


def get_top_server_players(top_type: str | None = "players") -> list[Any] | None:
    all_levels = get_demonlist()

    level_pos = {
        lvl["name"].lower(): lvl["placement"]
        for lvl in all_levels
    }

    level_points = {
        lvl["placement"]: float(lvl["points"])
        for lvl in all_levels
        if "placement" in lvl and "points" in lvl
    }

    def get_pos(level_name: str) -> int | None:
        return level_pos.get(level_name.lower())

    def get_positions(levels: list[str]) -> list[int]:
        pos = []

        for lvl in levels:
            p = get_pos(lvl)

            if p is not None:
                pos.append(p)

        return pos

    def get_level_points(pos: int) -> float:
        return level_points.get(pos, 0.0)

    players = get_players()

    players = [(name, info) for (name, info, _, _) in players]

    leaderboard_db = load_file("leaderboard")

    discord_players = []

    for name, info in players:

        raw_data = leaderboard_db.get(name)

        levels = normalize_levels(raw_data)
        levels = sorted(
            levels,
            key=lambda lvl: get_pos(lvl) if get_pos(lvl) is not None else float("inf")
        )

        points = round(sum(get_level_points(p) for p in get_positions(levels)), 2)

        discord_players.append((name, info, levels, points))


    if top_type == "players":
        return discord_players


    elif top_type == "by_hardest":

        def sort_key(p: list[Any]):
            _, _, levels, _ = p
            pos = get_positions(levels)

            return min(pos) if pos else float("inf")

        return sorted(discord_players, key=sort_key)


    if top_type == "by_list_points":

        def sort_key(p: list[Any]):
            _, _, _, points = p

            return -points

        return sorted(discord_players, key=sort_key)


    if top_type == "by_5_hardests":

        def sort_key(p: list[Any]):
            pos = sorted(get_positions(p[2]))

            if not pos:
                return float("inf")

            best = pos[:5]  # max 5 hardests
            return sum(best) / len(best)

        return sorted(discord_players, key=sort_key)


def get_top_completed_levels(limit: int | None = 10) -> list[tuple[str, int, int]]:
    all_levels = get_demonlist()

    level_pos = {
        lvl["name"].lower(): lvl["placement"]
        for lvl in all_levels
        if "name" in lvl and "placement" in lvl
    }

    def get_pos(level_name: str) -> int | None:
        return level_pos.get(level_name.lower())

    leaderboard_db = load_file("leaderboard")

    all_finished_levels = []

    for _, data in leaderboard_db.items():

        levels = normalize_levels(data)

        for lvl in levels:
            if get_pos(lvl) is not None:
                all_finished_levels.append(lvl)

    counter = Counter(all_finished_levels)

    result = []

    for lvl, count in counter.items():
        pos = get_pos(lvl)

        if pos is not None:
            result.append((lvl, pos, count))

    result.sort(key=lambda x: x[1])

    return result
