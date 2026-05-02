from flask import jsonify, render_template
import time
from flask import Flask
from src.logic.radio import radio
from src.routes.utils import logged_in, get_username


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

        for track in radio.schedule:
            start = track["start"]
            end = start + track["duration"]

            if start <= now <= end:
                filename = track["file"].split("/")[-1]
                if " - " in filename:
                    author, title = filename.rsplit(" - ", 1)
                    title = title.replace(".mp3", "")
                else:
                    author = "Unknown"
                    title = filename.replace(".mp3", "")

                return jsonify({
                    "file": track["file"],
                    "start": start,
                    "duration": track["duration"],
                    "title": title,
                    "author": author
                })

        return jsonify({"error": "nothing"})
