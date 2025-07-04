import requests

def load_list_from_py(url, variable_name):
    code = requests.get(url).text
    namespace = {}
    exec(code, namespace)
    return namespace[variable_name]

levels_url = "https://raw.githubusercontent.com/Gild56/gild56_website/main/static/lists/levels_list.py"
challenges_url = "https://raw.githubusercontent.com/Gild56/gild56_website/main/static/lists/challenges_list.py"
players_url = "https://raw.githubusercontent.com/Gild56/gild56_website/main/static/lists/players.py"

levels_list_top = load_list_from_py(levels_url, "levels_list_top")
challenges_list_top = load_list_from_py(challenges_url, "challenges_list_top")
players = load_list_from_py(players_url, "players")

print(levels_list_top)

level_points = {
    level[0]: (len(levels_list_top) - i) * 10
    for i, level in enumerate(levels_list_top)
}

top_players = []
for name, tag, passed_levels_1, passed_levels_2 in players:
    total_points = sum(level_points.get(lvl, 0) for lvl in passed_levels_1)
    top_players.append((name, tag, passed_levels_1, passed_levels_2, total_points))

top_players.sort(key=lambda x: x[4], reverse=True)


challenge_points = {
    challenge[0]: (len(challenges_list_top) - i) * 10
    for i, challenge in enumerate(challenges_list_top)
}

top_challenge_players = []
for name, tag, passed_levels_1, passed_levels_2 in players:
    challenge_score = sum(challenge_points.get(lvl, 0) for lvl in passed_levels_2)
    top_challenge_players.append((name, tag, passed_levels_1, passed_levels_2, challenge_score))

top_challenge_players.sort(key=lambda x: x[4], reverse=True)
