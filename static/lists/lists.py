import requests

def load_list_from_py(url, variable_name):
    code = requests.get(url).text
    namespace = {}
    exec(code, namespace)
    return namespace[variable_name]


def get_levels_list_top():
    levels_url = "https://raw.githubusercontent.com/Gild56/gild56_website_lists/main/levels_list.py"
    levels_list_top = load_list_from_py(levels_url, "levels_list_top")
    return levels_list_top

def get_challenges_list_top():
    challenges_url = "https://raw.githubusercontent.com/Gild56/gild56_website_lists/main/challenges_list.py"
    challenges_list_top = load_list_from_py(challenges_url, "challenges_list_top")
    return challenges_list_top

def get_players():
    players_url = "https://raw.githubusercontent.com/Gild56/gild56_website_lists/main/players.py"
    players = load_list_from_py(players_url, "players")
    return players


def get_top_players():
    levels_list_top = get_levels_list_top()
    challenges_list_top = get_challenges_list_top()
    players = get_players()

    level_points = {
        level[0]: (len(levels_list_top) - i) * 10
        for i, level in enumerate(levels_list_top)
    }

    top_players = []
    for name, tag, passed_levels_1, passed_levels_2 in players:
        total_points = sum(level_points.get(lvl, 0) for lvl in passed_levels_1)
        top_players.append((name, tag, passed_levels_1, passed_levels_2, total_points))

    top_players.sort(key=lambda x: x[4], reverse=True)

    return top_players


def get_top_challenge_players():
    levels_list_top = get_levels_list_top()
    challenges_list_top = get_challenges_list_top()
    players = get_players()

    challenge_points = {
        challenge[0]: (len(challenges_list_top) - i) * 10
        for i, challenge in enumerate(challenges_list_top)
    }

    top_challenge_players = []
    for name, tag, passed_levels_1, passed_levels_2 in players:
        challenge_score = sum(challenge_points.get(lvl, 0) for lvl in passed_levels_2)
        top_challenge_players.append((name, tag, passed_levels_1, passed_levels_2, challenge_score))

    top_challenge_players.sort(key=lambda x: x[4], reverse=True)

    return top_challenge_players
