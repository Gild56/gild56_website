from flask import Flask, request
from src.logic.ranking import get_points_by_place
from src.logic.ranking import get_top_players, get_player_ranks
from src.logic.data_loader import get_pos, load_file, get_demonlist
from src.routes.utils import get_mean, get_api
from typing import Any
import json
import urllib.request
import urllib.parse
import base64


def get_gd_level(level_id: int) -> dict[str, Any]:
    url = "https://www.boomlings.com/database/getGJLevels21.php"

    data = urllib.parse.urlencode({
        "str": str(level_id),
        "type": 10,
        "secret": "Wmfd2893gb7",
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"User-Agent": ""}
    )

    with urllib.request.urlopen(req) as response:
        raw = response.read().decode("utf-8")

    if raw == "-1":
        return {}

    sections = raw.split("#")
    if len(sections) < 5 or not sections[0]:
        return {}

    fields = sections[0].split("|")[0].split(":")
    level = dict(zip(fields[::2], fields[1::2]))

    try:
        description = base64.b64decode(
            level.get("3", "") + "=" * (-len(level.get("3", "")) % 4)
        ).decode("utf-8")
    except Exception:
        description = ""

    return {
        "id": int(level.get("1", 0)),
        "name": level.get("2", ""),
        "description": description,
        "version": int(level.get("5", 0)),
        "creator_id": int(level.get("6", 0)),
        "difficulty": int(level.get("9", 0)),
        "downloads": int(level.get("10", 0)),
        "official_song_id": int(level.get("12", 0)),
        "likes": int(level.get("14", 0)),
        "length": int(level.get("15", 0)),
        "stars": int(level.get("18", 0)),
        "featured": int(level.get("19", 0)),
        "raw": level,
    }


def register_new_api_routes(app: Flask):
    @app.route("/level/classic/get")
    def get_new_level() -> dict[str, Any]:
        try:
            ingame_id = request.args.get("ingame_id", None)
            if ingame_id is None:
                return {"message": "invalid_level_parameters", "data": {}}

            return {"message": "success", "data": get_level_data(ingame_id)}
        except Exception as e:
            return {"error": f"An error occured: {e}"}

    def get_level_data(ingame_id: str) -> dict[str, Any]:
        top = load_file("levels_list")
        index = None
        if ingame_id:
            index = next((i for i, item in enumerate(top) if item[1] == ingame_id), None)

        if index is None:
            return {"message": "level_not_found", "data": {}, "level": index}

        level_data = top[index]

        placement = index + 1

        keys = ["name", "ingame_id", "description", "completions"]
        data = dict(zip(keys, level_data))

        data["placement"] = placement
        data["points"] = get_points_by_place(placement)

        data["list_percent"] = 100
        data["creator"] = "GILD56"
        data["holder"] = "GILD56"

        data["copy_info"] = {}
        data["copy_info"]["is_copyable"] = True
        data["copy_info"]["password"] = None

        completions = data["completions"]
        data["completions"] = []
        position = 0
        for username, video in completions.items():
            completion_data = {
                "username": username,
                "video_url": f"https://youtu.be/{video}",
                "position": position,
                "percent": 100,
            }
            data["completions"].append(completion_data)
            position += 1

        verification = data["completions"][0]
        data["verification"] = {}
        data["verification"]["username"] = verification["username"]
        data["verification"]["video_url"] = verification["video_url"]
        data["verification"]["user_id"] = 0

        data["verifier"] = {}
        data["verifier"]["user_id"] = 0
        data["verifier"]["username"] = verification["username"]

        data["verification_url"] = verification["video_url"]

        data["id"] = "0"

        level_info = {} #temp get_gd_level(data["ingame_id"])

        data["length"] = level_info.get("length", 60)
        data["objects"] = level_info.get("objects", 5000)
        data["song_url"] = level_info.get("song_url", None)
        data["game_version"] = level_info.get("game_version", 2.2)
        data["date_created"] = level_info.get("date_created", "2026-10-05T02:21:45.414812Z")

        return data


    @app.route("/level/classic/list")
    def get_new_list() -> dict[str, Any]:
        levels = load_file("levels_list")
        return {"message": "level_not_found", "data": [get_level_data(level[1]) for level in levels]}


    @app.route("/user/get")
    def get_new_player(player: str) -> dict[str, Any]:
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


    @app.route("/leaderboard/user/list")
    def get_new_players() -> list[dict[str, Any]]:
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


    @app.route("/leaderboard/country/list")
    def get_new_countries() -> list[dict[str, Any]]:
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
