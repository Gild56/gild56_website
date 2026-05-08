from flask import Flask, render_template
from src.routes.utils import get_username, logged_in, get_len, get_mean
from src.logic.ranking import get_top_players, get_points_by_place
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
            def get_level_rank(
                level_name: str,
                top_list: list[tuple[str, str, str, str, dict[str, str]]]
            ):
                level_name = level_name.strip().lower()
                for i, level_data in enumerate(top_list):
                    name = level_data[0].strip().lower()
                    if name == level_name:
                        return i + 1

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

            keys = ["nickname", "id", "description", "gild_completion", "completions"]
            data = dict(zip(keys, list(player_data)))

            return data
        except StopIteration:
            return {"error": f"Player <{player}> not found"}
