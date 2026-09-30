from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, request
from src.routes.utils import get_username, logged_in, get_cube


def register_static_routes(app: Flask):
    @app.route("/")
    def index():
        return render_template(
            "other/index.html", logged_in=logged_in(),
            username=get_username(), get_cube=get_cube
        )


    @app.route("/tournaments")
    def tournaments():
        return render_template(
            "other/tournaments.html", logged_in=logged_in(),
            username=get_username()
        )


    @app.route("/contact")
    def contact():
        return render_template(
            "other/contact.html", logged_in=logged_in(),
            username=get_username()
        )


    @app.route("/hall_of_fame")
    def hall_of_fame():
        return render_template(
            "other/hall_of_fame.html", logged_in=logged_in(),
            username=get_username()
        )


    @app.route("/games")
    def games():
        return render_template(
            "other/games.html", logged_in=logged_in(),
            username=get_username()
        )


    @app.route("/jaime_les_ours")
    def jaime_les_ours():
        return render_template("other/jaime_les_ours.html")


    @app.route("/yameru")
    def yameru():
        return """<p secret="wp cjrt qjsWo dudtkd dmfh rktpdy">give up</p>"""


    @app.route("/dan-eo", methods=["GET", "POST"])
    def daneo():
        response = None

        if request.method == "POST":
            code = request.form.get("code", "").strip()

            responses = {
                "1234": "something is waiting"
            }

            response = responses.get(code, "invalid code")

        return f"""
        <form method="POST">
            <input type="text" name="code" placeholder="Enter code">
            <button type="submit">Submit</button>
        </form>
        {"<p>" + response + "</p>" if response else ""}
        """


    # Error pages

    @app.errorhandler(404)
    def handle_404(error: HTTPException):
        return render_template(
            "other/404.html",
            logged_in=logged_in(),
            username=get_username(),
            requested_url=request.url
        ), 404
