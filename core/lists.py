import urllib.request
import requests
from typing import Any

def load_list_from_py(variable_name: str, file_name: str) -> Any:
    try:
        with open(f"..\\gild56_website_lists\\{file_name}", "r", encoding="utf-8") as f:
            code = f.read()
    except:
        with urllib.request.urlopen(f"https://raw.githubusercontent.com/Gild56/gild56_website_lists/main/{file_name}") as response:
            code = response.read().decode('utf-8')
    namespace: dict[str, Any] = {}
    exec(code, namespace)
    return namespace[variable_name]


def get_leaderboard_db() -> Any:
    try:
        with open(f"..\\leaderboard\\leaderboard.json", "r", encoding="utf-8") as f:
            code = f.read()
    except:
        with urllib.request.urlopen(f"https://raw.githubusercontent.com/Gild56/gd_discord_leaderboard_maker/main/leaderboard.json") as response:
            code = response.read().decode('utf-8')
    code = "database = " + code
    namespace: dict[str, Any] = {}
    exec(code, namespace)
    return namespace["database"]


def get_levels_list_top() -> list[tuple[str, str, str, str, dict[str, str]]]:
    levels_list_top = load_list_from_py("levels_list_top", "levels_list.py")
    return levels_list_top


def get_challenges_list_top() -> list[tuple[str, str, str, str, dict[str, str]]]:
    challenges_list_top = load_list_from_py("challenges_list_top", "challenges_list.py")
    return challenges_list_top


def get_players() -> list[tuple[str, list[str], list[str], list[str]]]:
    players = load_list_from_py("players", "players.py")

    levels_list_top = get_levels_list_top()
    challenges_list_top = get_challenges_list_top()

    updated_players: list[tuple[str, list[str], list[str], list[str]]] = []

    for name, tag, passed_levels_1, passed_levels_2 in players:
        if name == "Gild56":
            passed_levels_1 = [
                level[0] for level in levels_list_top if level[3] != ""
            ]
        else:
            passed_levels_1 = [
                level[0] for level in levels_list_top if name in level[4]
            ]

        if name == "Gild56":
            passed_levels_2 = [
                challenge[0] for challenge in challenges_list_top if challenge[3] != ""
            ]
        else:
            passed_levels_2 = [
                challenge[0] for challenge in challenges_list_top if name in challenge[4]
            ]

        updated_players.append((name, tag, passed_levels_1, passed_levels_2))

    return updated_players


def get_points_by_place(rank: int) -> int:
    if rank == 1:
        return 60
    elif 2 <= rank <= 4:
        return 50
    elif 5 <= rank <= 10:
        return 30
    elif 11 <= rank <= 20:
        return 20
    else:
        return 10


def get_top_players() -> list[tuple[str, list[str], list[str], list[str], int]]:
    levels_list_top = get_levels_list_top()
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


def get_top_challenge_players() -> list[tuple[str, list[str], list[str], list[str], int]]:
    challenges_list_top = get_challenges_list_top()
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

def normalize_levels(data: Any) -> list[str]:
    if not data or len(data) < 2:
        return []

    levels_data = data[1]

    if isinstance(levels_data, dict):
        return list(levels_data.keys())

    if isinstance(levels_data, list):
        return levels_data

    return []


def get_demonlist() -> list[dict[str, Any]]:
    try:
        with open(f"..\\leaderboard\\top.txt", "r", encoding="utf-8") as f:
            code = f.read()
        code = "database = " + code
        namespace: dict[str, Any] = {}
        exec(code, namespace)
        all_levels = list(namespace["database"])
    except:
        response = requests.get("https://api.demonlist.org/level/classic/list")
        all_levels = response.json().get("data", {}).get("levels", [])

    if not all_levels:
        print("Error: No levels found.")
        return []

    # It removes Azurite by Royen by its id in the database
    # to keep Azurite by Sillow, that everybody beats (костыли)
    return [lvl for lvl in all_levels if lvl.get("id") != 2299]


def get_pos(level_name: str) -> int:
    all_levels = get_demonlist()
    level_pos = {
        lvl["name"].lower(): lvl["placement"]
        for lvl in all_levels
    }
    try:
        return level_pos[level_name.lower()]
    except KeyError:
        raise ValueError(f"Level doesn't exist: {level_name}")


def get_top_server_players(top_type: str | None = "by_hardest") -> list[Any] | None:
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

    leaderboard_db = get_leaderboard_db()

    discord_players = []

    for name, info in players:

        raw_data = leaderboard_db.get(name)
        levels = normalize_levels(raw_data) #todo sort by positions
        points = sum(get_level_points(p) for p in get_positions(levels))

        discord_players.append((name, info, levels, points))


    if top_type == "by_hardest":

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

            best = pos[:5]  # max 5 plus durs
            return sum(best) / len(best)

        return sorted(discord_players, key=sort_key)
