from flask import Flask, render_template, redirect, url_for, abort
from src.routes.utils import get_username, logged_in, get_len, get_mean
from src.logic.ranking import get_top_players, get_points_by_place
from src.logic.server_ranking import get_top_server_players, get_top_completed_levels
from src.logic.data_loader import get_pos, get_id, load_file


def register_list_routes(app: Flask):
    @app.route("/lists")
    def lists():
        return redirect(url_for('levels_list'))


    @app.route("/lists/gild/classic")
    def levels_list():
        return render_template(
            "list/list.html", logged_in=logged_in(),
            username=get_username(), levels=load_file("levels_list"),
            top="levels_list", get_points_by_place=get_points_by_place
        )


    @app.route("/lists/gild/challenges")
    def challenges_list():
        return render_template(
            "list/list.html", logged_in=logged_in(),
            username=get_username(), levels=load_file("challenges_list"),
            top="challenges_list", get_points_by_place=get_points_by_place
        )


    @app.route("/lists/server/classic")
    def server_levels_list():
        return render_template(
            "list/list.html", logged_in=logged_in(),
            username=get_username(), levels=load_file("server_levels_list"),
            top="server_levels_list", get_points_by_place=get_points_by_place
        )


    @app.route("/lists/server/challenges")
    def server_challenges_list():
        return render_template(
            "list/list.html", logged_in=logged_in(),
            username=get_username(), levels=load_file("server_challenges_list"),
            top="server_challenges_list", get_points_by_place=get_points_by_place
        )


    @app.route("/lists/gild/classic/<level>")
    def level_page(level: str):
        try:
            levels_list_top = load_file("levels_list")
            index = next(i for i, item in enumerate(levels_list_top) if item[0] == level)
            level_info = levels_list_top[index]

            return render_template(
                "list/level.html",
                logged_in=logged_in(),
                username=get_username(),
                level=level_info,
                level_position=index + 1,
                iter=iter, next=next
            )
        except StopIteration:
            return abort(404)


    @app.route("/lists/gild/challenges/<challenge>")
    def challenge_page(challenge: str):
        try:
            challenges_list_top = load_file("challenges_list")
            index = next(i for i, item in enumerate(challenges_list_top) if item[0] == challenge)
            level_info = challenges_list_top[index]

            return render_template(
                "list/level.html",
                logged_in=logged_in(),
                username=get_username(),
                level=level_info,
                level_position=index + 1,
                iter=iter, next=next
            )
        except StopIteration:
            return abort(404)


    @app.route("/lists/server/classic/<level>")
    def server_level_page(level: str):
        try:
            server_levels_list_top = load_file("server_levels_list")
            index = next(i for i, item in enumerate(server_levels_list_top) if item[0] == level)
            level_info = server_levels_list_top[index]

            return render_template(
                "list/level.html",
                logged_in=logged_in(),
                username=get_username(),
                level=level_info,
                level_position=index + 1,
                iter=iter, next=next
            )
        except StopIteration:
            return abort(404)


    @app.route("/lists/server/challenges/<challenge>")
    def server_challenge_page(challenge: str):
        try:
            server_challenges_list_top = load_file("server_challenges_list")
            index = next(i for i, item in enumerate(server_challenges_list_top) if item[0] == challenge)
            level_info = server_challenges_list_top[index]

            return render_template(
                "list/level.html",
                logged_in=logged_in(),
                username=get_username(),
                level=level_info,
                level_position=index + 1,
                iter=iter, next=next
            )
        except StopIteration:
            return abort(404)


    @app.route("/lists/server_leaderboard/top_levels")
    def server_leaderboard_top_levels():
        def generate_link(level: str):
            return f"https://thumbnails.demonlist.org/classic/{get_id(level)}.png"
        return render_template(
            "list/top_levels.html",
            logged_in=logged_in(),
            username=get_username(),
            top_completed_levels=get_top_completed_levels(),
            generate_link=generate_link
        )


    @app.route("/lists/server_leaderboard/by_hardest")
    def server_leaderboard_by_hardest():
        return render_template(
            "list/server_leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_server_players("by_hardest"),
            top_type="by_hardest", get_pos=get_pos, get_len=get_len
        )


    @app.route("/lists/server_leaderboard/by_list_points")
    def server_leaderboard_by_list_points():
        return render_template(
            "list/server_leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_server_players("by_list_points"),
            top_type="by_list_points", get_len=get_len, get_pos=get_pos
        )


    @app.route("/lists/server_leaderboard/by_5_hardests")
    def server_leaderboard_by_5_hardests():
        return render_template(
            "list/server_leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_server_players("by_5_hardests"),
            top_type="by_5_hardests", get_len=get_len, get_pos=get_pos, get_mean=get_mean
        )


    @app.route("/lists/gild/classic/leaderboard")
    def levels_leaderboard():
        return render_template(
            "list/leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_players("levels_list"),
            top="levels_list"
        )


    @app.route("/lists/gild/challenges/leaderboard")
    def challenges_leaderboard():
        return render_template(
            "list/leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_players("challenges_list"),
            top="challenges_list"
        )


    @app.route("/lists/server/classic/leaderboard")
    def server_levels_leaderboard():
        return render_template(
            "list/leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_players("levels_list"),
            top="server_levels_list"
        )


    @app.route("/lists/server/challenges/leaderboard")
    def server_challenges_leaderboard():
        return render_template(
            "list/leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_players("challenges_list"),
            top="server_challenges_list"
        )


    @app.route("/players/<player>")
    def player_page(player: str):
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

            return render_template(
                "list/player.html",
                logged_in=logged_in(),
                username=get_username(),
                player=player_data,
                challenges_points=challenges_points,
                levels_top_place=levels_top_place+1,
                challenges_top_place=challenges_top_place+1,
                server_levels_top_place=server_levels_top_place+1,
                server_challenges_top_place=server_challenges_top_place+1,
                challenges_list_top=load_file("challenges_list"),
                levels_list_top=load_file("levels_list"),
                get_level_rank=get_level_rank,
                extremes=extremes, get_len=get_len, get_pos=get_pos,
                server_levels_points=server_levels_points,
                server_challenges_points=server_challenges_points
            )
        except StopIteration:
            return abort(404)
