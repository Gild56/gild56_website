from flask import Flask, render_template, request
from src.routes.utils import get_username, logged_in
from src.logic.ranking import get_top_players
from src.logic.server_ranking import get_top_server_players, get_top_completed_levels
from src.logic.data_loader import get_pos, get_id, load_file
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
        data = []
        for level in levels:
            data.append(normalize_level(level[0], levels))
        return data


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

            levels_top_place = next(i for i, item in enumerate(top_players) if item[0] == player)
            challenges_top_place = next(i for i, item in enumerate(top_challenge_players) if item[0] == player)
            server_levels_top_place = next(i for i, item in enumerate(top_server_players) if item[0] == player)
            server_challenges_top_place = next(i for i, item in enumerate(top_server_challenge_players) if item[0] == player)

            player_data = top_players[levels_top_place]

            challenges_points = top_challenge_players[challenges_top_place][6]
            server_levels_points = top_server_players[server_levels_top_place][6]
            server_challenges_points = top_server_challenge_players[server_challenges_top_place][6]

            extremes = []
            top_server_players = get_top_server_players()
            for p in top_server_players:
                if p[0] == player:
                    extremes = p[2]

            keys = ["nickname", "data", "levels_list_completions", "challenges_list_completions", "server_levels_list_completions", "server_challenges_list_completions", "levels_list_points"]
            data: dict[str, Any] = dict(zip(keys, list(player_data)))

            data["youtube_channel"] = f"https://youtube.com/@{data["data"][0]}"
            data["country"] = data["data"][1]
            data["community_account"] = data["data"][2]
            data["description"] = data["data"][3]
            data["tag"] = data["data"][4]
            data.pop("data")

            data["challenges_list_points"] = challenges_points
            data["server_levels_list_points"] = server_levels_points
            data["server_challenges_list_points"] = server_challenges_points

            data["extremes"] = extremes

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

            player_data["extremes"] = {
                level: get_pos(level)
                for level in player_data.get("extremes", [])
            }

            data.append(player_data)

        sort_key = request.args.get("sort")

        if sort_key:
            data.sort(
                key=lambda x: x.get(sort_key, 0),
                reverse=True
            )

        return data
