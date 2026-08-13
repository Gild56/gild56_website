from flask import jsonify, render_template
import time
from flask import Flask
from src.logic.radio import radio
from src.routes.utils import logged_in, get_username
from urllib.parse import unquote


def register_radio_routes(app: Flask):

    @app.route("/radio")
    def radio_page():
        return render_template(
            "other/radio.html",
            logged_in=logged_in(),
            username=get_username()
        )

    @app.route("/radio/now")
    def radio_now():
        now = time.time()

        if radio.schedule and now > radio.schedule[-1]["start"] + radio.schedule[-1]["duration"]:
            radio.generate_schedule()

        for track in radio.schedule:
            start = track["start"]
            end = start + track["duration"]

            if start <= now <= end:

                filename = track["file"].split("/")[-1]
                filename = unquote(filename)

                if " - " in filename:
                    author, title = filename.rsplit(" - ", 1)
                    title = title.removesuffix(".mp3")
                else:
                    author = "Unknown"
                    title = filename.removesuffix(".mp3")

                return jsonify({
                    "file": track["file"],
                    "start": start,
                    "duration": track["duration"],
                    "title": title,
                    "author": author
                })

        return jsonify({"error": "nothing"})
