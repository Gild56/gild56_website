from werkzeug.exceptions import HTTPException
import os
from flask import Flask, render_template, redirect, url_for
from src.routes.utils import get_username, logged_in


def register_static_routes(app: Flask):
    @app.route("/")
    def index():
        return render_template(
            "index.html", logged_in=logged_in(),
            username=get_username()
        )


    @app.route("/contact")
    def contact():
        return render_template(
            "contact.html", logged_in=logged_in(),
            username=get_username()
        )


    @app.route("/hall_of_fame")
    def hall_of_fame():
        return render_template(
            "hall_of_fame.html", logged_in=logged_in(),
            username=get_username()
        )


    @app.route("/games")
    def games():
        return render_template(
            "games.html", logged_in=logged_in(),
            username=get_username()
        )


    @app.route("/jaime_les_ours")
    def jaime_les_ours():
        return render_template("jaime_les_ours.html")


    def flag_exists(code: str):
        path = os.path.join(app.static_folder, "images", "flags", f"{code}.png")
        return os.path.exists(path)
    app.jinja_env.globals.update(flag_exists=flag_exists)


    # Error pages

    @app.route("/404")
    def error404():
        return render_template(
            "404.html", logged_in=logged_in(),
            username=get_username()
        )


    @app.errorhandler(404)
    def handle_404(_error: HTTPException):
        return redirect(url_for('error404'))
