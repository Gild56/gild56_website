from flask import Flask, render_template, request
from src.routes.utils import get_username, logged_in
from src.logic.ranking import get_top_players, get_player_ranks
from src.logic.data_loader import get_pos, load_file, get_demonlist
from src.routes.utils import get_mean, get_api
from collections import Counter
from typing import Any
import json


def register_api_routes(app: Flask):
    def normalize_level(level:str, top: dict[str, Any]) -> dict[str, Any]:
        try:
            index = next(i for i, item in enumerate(top) if item[0] == level)

            level_data = top[index]

            position = index + 1

            keys = ["name", "id", "description", "completions"]
            data = dict(zip(keys, level_data))

            data["position"] = position

            return data
        except:
            return {"error": f"Level <{level}> not found"}


    def normalize_levels(levels: dict[str, Any]) -> list[dict[str, Any]]:
        return [normalize_level(level[0], levels) for level in levels]


    @app.route("/api")
    def api():
        return render_template(
            "other/api.html", logged_in=logged_in(),
            username=get_username()
        )


    @app.route("/api/lists/gild/classic")
    def get_levels_list() -> list[dict[str, Any]]:
        return normalize_levels(load_file("levels_list"))

    @app.route("/api/lists/gild/challenges")
    def get_challenges_list() -> list[dict[str, Any]]:
        return normalize_levels(load_file("challenges_list"))

    @app.route("/api/lists/server/classic")
    def get_server_levels_list() -> list[dict[str, Any]]:
        return normalize_levels(load_file("server_levels_list"))

    @app.route("/api/lists/server/challenges")
    def get_server_challenges_list() -> list[dict[str, Any]]:
        return normalize_levels(load_file("server_challenges_list"))


    @app.route("/api/lists/gild/classic/levels/<level>")
    def get_level(level: str):
        return normalize_level(level, load_file("levels_list"))

    @app.route("/api/lists/gild/challenges/levels/<level>")
    def get_challenge(level: str):
        return normalize_level(level, load_file("challenges_list"))

    @app.route("/api/lists/server/classic/levels/<level>")
    def get_server_level(level: str):
        return normalize_level(level, load_file("server_levels_list"))

    @app.route("/api/lists/server/challenges/levels/<level>")
    def get_server_challenge(level: str):
        return normalize_level(level, load_file("server_challenges_list"))


    @app.route("/api/lists/players/<player>")
    def get_player(player: str) -> dict[str, Any]:
        try:
            top_players = get_top_players()

            player_data = next(
                item for item in top_players
                if item[0] == player
            )

            ranks = get_player_ranks()

            leaderboard_db = load_file("leaderboard")

            raw_data = leaderboard_db.get(player)

            if raw_data:
                levels_data = raw_data[1]

                if isinstance(levels_data, dict):
                    extremes = list(levels_data.keys())
                elif isinstance(levels_data, list):
                    extremes = levels_data
                else:
                    extremes = []
            else:
                extremes = []

            keys = ["nickname", "data", "levels_list_completions", "challenges_list_completions", "server_levels_list_completions", "server_challenges_list_completions", "levels_list_points", "challenges_list_points", "server_levels_list_points", "server_challenges_list_points"]
            data: dict[str, Any] = dict(zip(keys, list(player_data)))

            data["youtube_channel"] = data['data'][0]
            data["country"] = data["data"][1]
            data["description"] = data["data"][2]
            data["tag"] = data["data"][3]
            data.pop("data")

            data["levels_list_place"] = ranks["levels_list_place"][player]
            data["challenges_list_place"] = ranks["challenges_list_place"][player]
            data["server_levels_list_place"] = ranks["server_levels_list_place"][player]
            data["server_challenges_list_place"] = ranks["server_challenges_list_place"][player]

            data["extremes"] = extremes
            data["extremes"] = {
                level: get_pos(level)
                for level in data.get("extremes", [])
            }

            if data["extremes"]:
                data["hardest_pos"] = min(data["extremes"].values())
                hardest_name, hardest_position = min(
                    data["extremes"].items(),
                    key=lambda x: x[1]
                )

                data["hardest"] = {
                    "name": hardest_name,
                    "position": hardest_position
                }

                all_levels = get_demonlist()

                level_points = {
                    lvl["placement"]: float(lvl["points"])
                    for lvl in all_levels
                    if "placement" in lvl and "points" in lvl
                }

                data["list_points"] = round(
                    sum(
                        level_points.get(pos, 0.0)
                        for pos in data["extremes"].values()
                    ),
                    2
                )

                if len(data["extremes"]) >= 5:
                    positions = sorted(data["extremes"].values())[:5]
                    data["5_hardests_mean"] = (
                        get_mean(positions)
                        if positions else None
                    )

                    top5 = sorted(data["extremes"].items(), key=lambda x: x[1])[:5]

                    data["5_hardests"] = [
                        {"name": name, "position": pos}
                        for name, pos in top5
                    ]
                else:
                    data["5_hardests_mean"] = None
                    data["5_hardests"] = None

            else:
                data["hardest"] = None
                data["hardest_pos"] = None
                data["5_hardests_mean"] = None
                data["5_hardests"] = None
                data["list_points"] = 0

            return data

        except KeyError:
            return {"error": f"Player <{player}> not found"}

        except StopIteration:
            return {"error": f"Error processing the player <{player}>"}


    @app.route("/api/lists/players")
    def get_players() -> list[dict[str, Any]]:
        players = []

        for player in get_top_players():
            player_data = get_player(player[0])
            players.append(player_data)

        sort_key = request.args.get("sort")
        reverse = request.args.get("reverse", "true").lower() == "true"

        if sort_key:
            players.sort(
                key=lambda x: (
                    x.get(sort_key) is None,
                    x.get(sort_key)
                )
            )

        if reverse:
            players.reverse()

        return players


    @app.route("/api/lists/countries")
    def get_countries() -> list[dict[str, Any]]:
        countries = []

        with open("static/images/flags/country_names_list.json", "r", encoding="utf-8") as f:
            country_names_list = json.load(f)

        players = get_api(f"{request.host_url}api/lists/players")

        for player in players:
            country_code = player["country"]

            country_index = None

            for i, country in enumerate(countries):
                if country["code"] == country_code:
                    country_index = i
                    break

            if country_index is None:
                countries.append(
                    {
                        "code": country_code,
                        "name": country_names_list.get(country_code, country_code),
                        "levels_list_points": 0,
                        "challenges_list_points": 0,
                        "server_levels_list_points": 0,
                        "server_challenges_list_points": 0,
                        "players_count": 0,
                        "players": []
                    }
                )

                country_index = len(countries) - 1

            player_stats = {
                "nickname": player["nickname"],
                "levels_list_points": player["levels_list_points"],
                "challenges_list_points": player["challenges_list_points"],
                "server_levels_list_points": player["server_levels_list_points"],
                "server_challenges_list_points": player["server_challenges_list_points"]
            }

            countries[country_index]["levels_list_points"] += player["levels_list_points"]
            countries[country_index]["challenges_list_points"] += player["challenges_list_points"]
            countries[country_index]["server_levels_list_points"] += player["server_levels_list_points"]
            countries[country_index]["server_challenges_list_points"] += player["server_challenges_list_points"]
            countries[country_index]["players_count"] += 1
            countries[country_index]["players"].append(player_stats)

        ranking_keys = [
            ("levels_list_points", "levels_list_place"),
            ("challenges_list_points", "challenges_list_place"),
            ("server_levels_list_points", "server_levels_list_place"),
            ("server_challenges_list_points", "server_challenges_list_place"),
        ]

        for points_key, place_key in ranking_keys:
            sorted_countries = sorted(
                countries,
                key=lambda country: country[points_key],
                reverse=True
            )

            for place, country in enumerate(sorted_countries, start=1):
                country[place_key] = place

        sort_key = request.args.get("sort")
        reverse = request.args.get("reverse", "true").lower() == "true"

        if sort_key:
            countries.sort(
                key=lambda x: (
                    x.get(sort_key) is None,
                    x.get(sort_key)
                )
            )

        if reverse:
            countries.reverse()

        return countries


    @app.route("/api/lists/top_completed_extremes")
    def get_top_completed_extremes() -> list[Any]:
        def normalize_extremes(data: Any) -> list[str]:
            if not data or len(data) < 2:
                return []

            levels_data = data[1]

            if isinstance(levels_data, dict):
                return list(levels_data.keys())

            if isinstance(levels_data, list):
                return levels_data

            return []
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

            levels = normalize_extremes(data)

            all_finished_levels.extend(
                lvl for lvl in levels
                if get_pos(lvl) is not None
            )

        counter = Counter(all_finished_levels)

        result = []

        for lvl, count in counter.items():
            pos = get_pos(lvl)

            if pos is not None:
                result.append({
                    "name": lvl,
                    "position": pos,
                    "completions": count
                })

        result.sort(key=lambda x: x["position"])

        return result
