import os
import random
import time
from typing import Any
from mutagen.mp3 import MP3
import requests

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../static/radio"))

music_dir = os.path.join(BASE_DIR, "music")
podcast_dir = os.path.join(BASE_DIR, "podcasts")
ads_dir = os.path.join(BASE_DIR, "ads")

NEWS_URL = "https://raw.githubusercontent.com/Gild56/gild56_website_lists/main/Gild56 - News.mp3"
news_file = os.path.join(podcast_dir, "news.mp3")

def update_news():
    try:
        tmp_file = news_file + ".tmp"

        r = requests.get(NEWS_URL, timeout=10)
        r.raise_for_status()

        with open(tmp_file, "wb") as f:
            f.write(r.content)

        os.replace(tmp_file, news_file)

    except Exception as e:
        print(f"[News] Update failed: {e}")

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
podcasts = list_mp3(podcast_dir, exclude=["news.mp3"])
ads = list_mp3(ads_dir)


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

        while len(self.schedule) < 200:
            last_music = None

            next_hour = int(start - (start % 3600) + 3600)

            while start < next_hour:
                music_file = random.choice(music)

                while music_file == last_music:
                    music_file = random.choice(music)

                last_music = music_file
                start = self.add(music_file, start)
                start = self.add(None, start, pause=5)

            start = self.add(news_file, next_hour)
            start = self.add(None, start, pause=5)

            start = self.add(random.choice(ads), start)
            start = self.add(None, start, pause=5)

            for _ in range(3):
                start = self.add(random.choice(podcasts), start)
                start = self.add(None, start, pause=5)
                start = self.add(random.choice(ads), start)
                start = self.add(None, start, pause=5)

            start = self.add(random.choice(ads), start)
            start = self.add(None, start, pause=5)
            start = self.add(random.choice(ads), start)
            start = self.add(None, start, pause=5)

            start = self.add(random.choice(music), start)
            start = self.add(None, start, pause=5)
            start = self.add(random.choice(ads), start)
            start = self.add(None, start, pause=5)
            start = self.add(random.choice(ads), start)
            start = self.add(None, start, pause=5)


update_news()
radio = RadioScheduler()
