from core.data_loader import load_list_from_py

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