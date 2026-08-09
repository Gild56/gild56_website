import random
import time
import urllib.request
import json
import tempfile
import os

from urllib.parse import quote
from mutagen.mp3 import MP3


MUSIC_URL = "https://raw.githubusercontent.com/Gild56/gild56_website_lists/refs/heads/main/music"
COVERS_URL = "https://raw.githubusercontent.com/Gild56/gild56_website_lists/refs/heads/main/images/covers"


def get_duration(url: str) -> float:
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
        temp_path = temp.name

    try:
        urllib.request.urlretrieve(url, temp_path)
        return MP3(temp_path).info.length
    finally:
        os.remove(temp_path)


def get_song(song: str) -> str:
    return f"{MUSIC_URL}/{quote(song)}"


def get_cover(author: str) -> str:
    return f"{COVERS_URL}/{quote(author)}.png"


def get_all_songs():
    url = "https://api.github.com/repos/Gild56/gild56_website_lists/contents/music"

    token = os.getenv("GITHUB_TOKEN")

    headers = {
        "User-Agent": "Gild56-Website"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request) as response:
        data = json.load(response)

    return [
        file["name"].removesuffix(".mp3")
        for file in data
        if file["name"].endswith(".mp3")
    ]


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

        # URL GitHub
        web_path = get_song(path)

        # Durée du MP3
        duration = get_duration(web_path)

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
