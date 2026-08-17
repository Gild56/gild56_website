from flask import Flask, render_template, redirect, url_for, abort, request
from src.routes.utils import get_username, logged_in, get_len, get_mean, get_cube, get_thumbnail
from src.logic.ranking import get_points_by_place
from src.logic.data_loader import get_pos, get_id
import json
from urllib.request import urlopen
from urllib.parse import quote

def get_api(route: str):
    route = quote(route, safe=":/?=&")

    with urlopen(route) as response:
        return json.load(response)



def register_list_routes(app: Flask):
    @app.route("/lists")
    def lists():
        return redirect(url_for('levels_list'))


    @app.route("/lists/gild/classic")
    def levels_list():
        return render_template(
            "list/list.html", logged_in=logged_in(),
            username=get_username(), levels=get_api(f"{request.host_url}api/lists/gild/classic"),
            top="levels_list", get_points_by_place=get_points_by_place,
            iter=iter, next=next, get_thumbnail=get_thumbnail
        )


    @app.route("/lists/gild/challenges")
    def challenges_list():
        return render_template(
            "list/list.html", logged_in=logged_in(),
            username=get_username(), levels=get_api(f"{request.host_url}api/lists/gild/challenges"),
            top="challenges_list", get_points_by_place=get_points_by_place,
            iter=iter, next=next, get_thumbnail=get_thumbnail
        )


    @app.route("/lists/server/classic")
    def server_levels_list():
        return render_template(
            "list/list.html", logged_in=logged_in(),
            username=get_username(), levels=get_api(f"{request.host_url}api/lists/server/classic"),
            top="server_levels_list", get_points_by_place=get_points_by_place,
            iter=iter, next=next, get_thumbnail=get_thumbnail
        )


    @app.route("/lists/server/challenges")
    def server_challenges_list():
        return render_template(
            "list/list.html", logged_in=logged_in(),
            username=get_username(), levels=get_api(f"{request.host_url}api/lists/server/challenges"),
            top="server_challenges_list", get_points_by_place=get_points_by_place,
            iter=iter, next=next, get_thumbnail=get_thumbnail
        )


    @app.route("/lists/gild/classic/levels/<level>")
    def level_page(level: str):
        try:
            level_info = get_api(f"{request.host_url}api/lists/gild/classic/levels/{level}")

            return render_template(
                "list/level.html",
                logged_in=logged_in(),
                username=get_username(),
                level=level_info,
                iter=iter, next=next,
                get_cube=get_cube
            )
        except StopIteration:
            return abort(404)


    @app.route("/lists/gild/challenges/levels/<challenge>")
    def challenge_page(challenge: str):
        try:
            level_info = get_api(f"{request.host_url}api/lists/gild/challenges/levels/{challenge}")

            return render_template(
                "list/level.html",
                logged_in=logged_in(),
                username=get_username(),
                level=level_info,
                iter=iter, next=next,
                get_cube=get_cube
            )
        except StopIteration:
            return abort(404)


    @app.route("/lists/server/classic/levels/<level>")
    def server_level_page(level: str):
        try:
            level_info = get_api(f"{request.host_url}api/lists/server/classic/levels/{level}")

            return render_template(
                "list/level.html",
                logged_in=logged_in(),
                username=get_username(),
                level=level_info,
                iter=iter, next=next
            )
        except StopIteration:
            return abort(404)


    @app.route("/lists/server/challenges/levels/<challenge>")
    def server_challenge_page(challenge: str):
        try:
            level_info = get_api(f"{request.host_url}api/lists/server/challenges/levels/{challenge}")

            return render_template(
                "list/level.html",
                logged_in=logged_in(),
                username=get_username(),
                level=level_info,
                iter=iter, next=next
            )
        except StopIteration:
            return abort(404)


    @app.route("/lists/server_leaderboard/top_levels")
    def server_leaderboard_top_levels():

        def generate_gdl_thumbnail_link(level: str):
            return f"https://thumbnails.demonlist.org/classic/{get_id(level)}.png"

        return render_template(
            "list/top_levels.html",
            logged_in=logged_in(),
            username=get_username(),
            top_completed_levels=get_api(f"{request.host_url}api/lists/top_completed_extremes"),
            generate_gdl_thumbnail_link=generate_gdl_thumbnail_link
        )


    @app.route("/lists/server_leaderboard/by_hardest")
    def server_leaderboard_by_hardest():
        return render_template(
            "list/server_leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_api(f"{request.host_url}api/lists/players?sort=hardest_pos&reverse=false"),
            top_type="by_hardest", get_pos=get_pos, get_len=get_len, get_cube=get_cube
        )


    @app.route("/lists/server_leaderboard/by_list_points")
    def server_leaderboard_by_list_points():
        return render_template(
            "list/server_leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_api(f"{request.host_url}api/lists/players?sort=list_points"),
            top_type="by_list_points", get_len=get_len, get_pos=get_pos, get_cube=get_cube
        )


    @app.route("/lists/server_leaderboard/by_5_hardests")
    def server_leaderboard_by_5_hardests():
        return render_template(
            "list/server_leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_api(f"{request.host_url}api/lists/players?sort=5_hardests_mean&reverse=false"),
            top_type="by_5_hardests", get_len=get_len, get_pos=get_pos, get_mean=get_mean
        )


    @app.route("/lists/gild/classic/leaderboard")
    def levels_leaderboard():
        return render_template(
            "list/leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_api(f"{request.host_url}api/lists/players?sort=levels_list_points"),
            top="levels_list", get_cube=get_cube
        )


    @app.route("/lists/gild/challenges/leaderboard")
    def challenges_leaderboard():
        return render_template(
            "list/leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_api(f"{request.host_url}api/lists/players?sort=challenges_list_points"),
            top="challenges_list", get_cube=get_cube
        )


    @app.route("/lists/server/classic/leaderboard")
    def server_levels_leaderboard():
        return render_template(
            "list/leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_api(f"{request.host_url}api/lists/players?sort=server_levels_list_points"),
            top="server_levels_list", get_cube=get_cube
        )


    @app.route("/lists/server/challenges/leaderboard")
    def server_challenges_leaderboard():
        return render_template(
            "list/leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_api(f"{request.host_url}api/lists/players?sort=server_challenges_list_points"),
            top="server_challenges_list", get_cube=get_cube
        )


    @app.route("/players/<player>")
    def player_page(player: str):
        try:
            def get_level_rank(level_name: str, top: str) -> int | None:
                level_data = get_api(f"{request.host_url}api/lists/{top}/levels/{level_name}")
                position = level_data.get("position", None)
                if position:
                    return position
                else:
                    return None

            player_data = get_api(f"{request.host_url}api/lists/players/{player}")

            return render_template(
                "list/player.html",
                logged_in=logged_in(),
                username=get_username(),
                player=player_data,
                get_level_rank=get_level_rank,
                get_len=get_len, get_pos=get_pos,
                get_cube=get_cube
            )
        except:
            return abort(404)


    @app.route("/lists/roulette")
    def roulette_page():
        return render_template(
            "list/roulette.html",
            logged_in=logged_in(),
            username=get_username(),
            list_levels=get_api(f"{request.host_url}api/lists/gild/classic"),
            challenges_levels=get_api(f"{request.host_url}api/lists/gild/challenges"),
            server_list_levels=get_api(f"{request.host_url}api/lists/server/classic"),
            server_challenges_levels=get_api(f"{request.host_url}api/lists/server/challenges")
        )
