from flask import Flask, render_template, redirect, url_for
from src.routes.utils import get_username, logged_in, get_len, get_mean
from src.logic.players import get_levels_list, get_challenges_list
from src.logic.ranking import get_top_players, get_top_challenge_players, get_points_by_place
from src.logic.server_ranking import get_top_server_players
from src.logic.data_loader import get_pos


def register_list_routes(app: Flask):
    @app.route("/lists")
    def lists():
        return redirect(url_for('levels_list'))


    @app.route("/lists/levels")
    def levels_list():
        return render_template(
            "list.html", logged_in=logged_in(),
            username=get_username(), levels=get_levels_list(),
            top="levels", get_points_by_place=get_points_by_place
        )


    @app.route("/lists/levels/<level>")
    def level_page(level: str):
        try:
            levels_list_top = get_levels_list()
            index = next(
                i for i, item in enumerate(levels_list_top) if item[0] == level)
            level_info = levels_list_top[index]

            return render_template(
                "level.html",
                logged_in=logged_in(),
                username=get_username(),
                level=level_info,
                level_position=index + 1
            )
        except StopIteration:
            return redirect(url_for('error404'))


    @app.route("/lists/challenges")
    def challenges_list():
        return render_template(
            "list.html", logged_in=logged_in(),
            username=get_username(), levels=get_challenges_list(),
            top="challenges", get_points_by_place=get_points_by_place
        )


    @app.route("/lists/challenges/<challenge>")
    def challenge_page(challenge: str):
        try:
            challenges_list_top = get_challenges_list()
            index = next(
                i for i, item in enumerate(
                    challenges_list_top) if item[0] == challenge)
            level_info = challenges_list_top[index]

            return render_template(
                "level.html",
                logged_in=logged_in(),
                username=get_username(),
                level=level_info,
                level_position=index + 1
            )
        except StopIteration:
            return redirect(url_for('error404'))


    @app.route("/lists/server_leaderboard/by_hardest")
    def server_leaderboard_by_hardest():
        return render_template(
            "server_leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_server_players("by_hardest"),
            top_type="by_hardest", get_pos=get_pos, get_len=get_len
        )


    @app.route("/lists/server_leaderboard/by_list_points")
    def server_leaderboard_by_list_points():
        return render_template(
            "server_leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_server_players("by_list_points"),
            top_type="by_list_points", get_len=get_len, get_pos=get_pos
        )


    @app.route("/lists/server_leaderboard/by_5_hardests")
    def server_leaderboard_by_5_hardests():
        return render_template(
            "server_leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_server_players("by_5_hardests"),
            top_type="by_5_hardests", get_len=get_len, get_pos=get_pos, get_mean=get_mean
        )


    @app.route("/lists/leaderboard")
    def leaderboard():
        return render_template(
            "leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_players(),
            top="levels"
        )


    @app.route("/lists/challenges_leaderboards")
    def challenges_leaderboard():
        return render_template(
            "leaderboard.html",
            logged_in=logged_in(),
            username=get_username(),
            players=get_top_challenge_players(),
            top="challenges"
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

            top_players = get_top_players()
            top_challenge_players = get_top_challenge_players()

            levels_top_place = next(
                i for i, item in enumerate(top_players) if item[0] == player)
            challenges_top_place = next(
                i for i, item in enumerate(
                    top_challenge_players) if item[0] == player)
            player_data = top_players[levels_top_place]
            challenges_profile = top_challenge_players[challenges_top_place]
            challenges_points = challenges_profile[4]

            extremes = []
            top_server_players = get_top_server_players()
            for p in top_server_players:
                if p[0] == player:
                    extremes = p[2]

            return render_template(
                "player.html",
                logged_in=logged_in(),
                username=get_username(),
                player=player_data,
                challenges_points=challenges_points,
                levels_position=levels_top_place+1,
                challenges_position=challenges_top_place+1,
                challenges_list_top=get_challenges_list(),
                levels_list_top=get_levels_list(),
                get_level_rank=get_level_rank,
                extremes=extremes, get_len=get_len, get_pos=get_pos
            )
        except StopIteration:
            return redirect(url_for('error404'))
