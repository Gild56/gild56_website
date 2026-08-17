import random
import time
import json
import urllib.request
import os
from urllib.parse import quote
import base64


MUSIC_URL = "https://raw.githubusercontent.com/Gild56/gild56_website_lists/refs/heads/main/music"
COVERS_URL = "https://raw.githubusercontent.com/Gild56/gild56_website_lists/refs/heads/main/images/covers"
DURATIONS_URL = "https://api.github.com/repos/Gild56/gild56_website_lists/contents/json/song_durations.json"


def get_song(song: str) -> str:
    return f"{MUSIC_URL}/{quote(song, safe='')}.mp3"


def get_cover(author: str) -> str:
    return f"{COVERS_URL}/{quote(author, safe='')}.png"


def get_song_durations():
    token = os.getenv("GITHUB_TOKEN")

    headers = {
        "User-Agent": "Gild56-Website",
        "Accept": "application/vnd.github+json"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(
        DURATIONS_URL,
        headers=headers
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.load(response)

    content = base64.b64decode(data["content"]).decode("utf-8")

    return json.loads(content)


def get_all_songs():
    return [
        filename.removesuffix(".mp3")
        for filename in song_durations
        if filename.endswith(".mp3")
    ]


song_durations = get_song_durations()
music = get_all_songs()


class RadioScheduler:

    def __init__(self):
        self.schedule = []
        self.generate_schedule()

    def reload(self):
        self.schedule = []
        self.generate_schedule()

    def add(
        self,
        path: str | None,
        start: float,
        pause: float = 0
    ):
        if path is None:
            self.schedule.append({
                "file": None,
                "start": start,
                "duration": pause
            })

            return start + pause

        web_path = get_song(path)

        filename = f"{path}.mp3"

        duration = song_durations.get(filename)

        if duration is None:
            raise ValueError(
                f"Can't find duration for the song {filename}"
            )

        self.schedule.append({
            "file": web_path,
            "start": start,
            "duration": duration
        })

        return start + duration

    def generate_schedule(self):
        start = time.time()
        end_time = start + 3600

        while start < end_time:
            song = random.choice(music)

            start = self.add(song, start)
            start = self.add(None, start, pause=5)


radio = RadioScheduler()
