from flask import Flask, render_template, request
from src.routes.utils import get_username, logged_in
from src.logic.ranking import get_top_players
from src.logic.server_ranking import get_top_server_players, get_demonlist
from src.logic.data_loader import get_pos, load_file
from src.routes.utils import get_mean
from collections import Counter
from typing import Any


def register_api_routes(app: Flask):
    def normalize_level(level:str, top: dict[str, Any]) -> dict[str, Any]:
        try:
            position = next(i for i, item in enumerate(top) if item[0] == level)

            level_data = top[position]

            keys = ["name", "id", "description", "gild_completion", "completions"]
            data = dict(zip(keys, level_data))
            gild = data.pop("gild_completion", None)

            data["position"] = position

            data["completions"] = {
                k: f"https://youtube.com/?watch={v}" if isinstance(v, str) else v
                for k, v in data["completions"].items()
            }

            if gild:
                data.setdefault("completions", {})
                data["completions"]["Gild56"] = gild

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


    @app.route("/api/lists/gild/classic/<level>")
    def get_level(level: str):
        return normalize_level(level, load_file("levels_list"))


    @app.route("/api/lists/gild/challenge/<level>")
    def get_challenge(level: str):
        return normalize_level(level, load_file("challenges_list"))


    @app.route("/api/lists/server/classic/<level>")
    def get_server_level(level: str):
        return normalize_level(level, load_file("server_levels_list"))


    @app.route("/api/lists/server/challenge/<level>")
    def get_server_challenge(level: str):
        return normalize_level(level, load_file("server_challenges_list"))


    @app.route("/api/players/<player>")
    def get_player(player: str) -> dict[str, Any]:
        try:
            top_players = get_top_players("levels_list")
            top_challenge_players = get_top_players("challenges_list")
            top_server_players = get_top_players("server_levels_list")
            top_server_challenge_players = get_top_players("server_challenges_list")

            levels_top_places = {
                item[0]: i
                for i, item in enumerate(top_players)
            }
            levels_top_place = levels_top_places[player]

            challenges_top_places = {
                item[0]: i
                for i, item in enumerate(top_challenge_players)
            }
            challenges_top_place = challenges_top_places[player]

            server_levels_top_places = {
                item[0]: i
                for i, item in enumerate(top_server_players)
            }
            server_levels_top_place = server_levels_top_places[player]

            server_challenges_top_places = {
                item[0]: i
                for i, item in enumerate(top_server_challenge_players)
            }
            server_challenges_top_place = server_challenges_top_places[player]

            player_data = top_players[levels_top_place]

            challenges_points = top_challenge_players[challenges_top_place][6]
            server_levels_points = top_server_players[server_levels_top_place][6]
            server_challenges_points = top_server_challenge_players[server_challenges_top_place][6]

            extremes = []
            top_server_extreme_players = get_top_server_players()
            for p in top_server_extreme_players:
                if p[0] == player:
                    extremes = p[2]

            keys = ["nickname", "data", "levels_list_completions", "challenges_list_completions", "server_levels_list_completions", "server_challenges_list_completions", "levels_list_points"]
            data: dict[str, Any] = dict(zip(keys, list(player_data)))

            data["youtube_channel"] = f"https://youtube.com/{data['data'][0]}"
            data["country"] = data["data"][1]
            data["community_account"] = data["data"][2]
            data["description"] = data["data"][3]
            data["tag"] = data["data"][4]
            data.pop("data")

            data["challenges_list_points"] = challenges_points
            data["server_levels_list_points"] = server_levels_points
            data["server_challenges_list_points"] = server_challenges_points

            data["extremes"] = extremes
            data["extremes"] = {
                level: get_pos(level)
                for level in data.get("extremes", [])
            }

            if data["extremes"]:
                data["hardest"] = min(data["extremes"].values())

                if len(data["extremes"]) >= 5:
                    positions = sorted(data["extremes"].values())[:5]
                    data["5_hardests"] = (
                        get_mean(positions)
                        if positions else None
                    )
                else:
                    data["5_hardests"] = None

            else:
                data["hardest"] = None
                data["5_hardests"] = None
                data["list_points"] = 0

            data["levels_list_place"] = levels_top_place + 1
            data["challenges_list_place"] = challenges_top_place + 1
            data["server_levels_list_place"] = server_levels_top_place + 1
            data["server_challenges_list_place"] = server_challenges_top_place + 1

            return data
        except StopIteration:
            return {"error": f"Player <{player}> not found"}


    @app.route("/api/players")
    def get_players() -> list[dict[str, Any]]:
        data = []

        for player in get_top_players("levels_list"):
            player_data = get_player(player[0])
            data.append(player_data)

        sort_key = request.args.get("sort")
        reverse = request.args.get("reverse", "true").lower() == "true"

        if sort_key:
            data.sort(
                key=lambda x: (
                    x.get(sort_key) is None,
                    x.get(sort_key)
                )
            )

        if reverse:
            data.reverse()

        return data


    @app.route("/api/top_completed_extremes")
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
