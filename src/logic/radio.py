import os
import random
import time
from typing import Any
from mutagen.mp3 import MP3

music_dir = "static/radio/music/"

def get_duration(path: str):
    return MP3(path).info.length


def list_mp3(folder: str, exclude: list[str] | None = None) -> list[Any]:
    files = []
    for f in os.listdir(folder):
        if f.endswith(".mp3"):
            if exclude and f in exclude:
                continue
            files.append(os.path.join(folder, f))
    return files


music = list_mp3(music_dir)


class RadioScheduler:

    def __init__(self):
        self.schedule = []
        self.generate_schedule()

    def reload(self):
        self.schedule = []
        self.generate_schedule()

    def add(self, path: str | None, start: int, pause: float = 0):

        if path is None:
            self.schedule.append({
                "file": None,
                "start": start,
                "duration": pause
            })
            return start + pause

        duration = get_duration(path)

        web_path = path.split("static")[1].replace("\\", "/")

        self.schedule.append({
            "file": "static" + web_path,
            "start": start,
            "duration": duration
        })

        return start + duration


    def generate_schedule(self):
        start = time.time()
        end_time = start + 3600

        while start < end_time:
            start = self.add(random.choice(music), start)
            start = self.add(None, start, pause=5)

radio = RadioScheduler()
