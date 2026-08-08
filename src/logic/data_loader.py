import urllib.request
from typing import Any
import threading
import json
import time
from functools import lru_cache


@lru_cache
def load_file(file_name: str) -> Any:
    url = f"https://raw.githubusercontent.com/Gild56/gild56_website_lists/main/json/{file_name}.json"

    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")

    return json.loads(data)


@lru_cache
def get_demonlist() -> list[dict[str, Any]]:
    url = "https://api.demonlist.org/level/classic/list"

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(req) as response:
        data = response.read().decode("utf-8")
        json_data = json.loads(data)
        all_levels = json_data.get("data", {}).get("levels", [])

    # It removes Azurite by Royen by its id in the database
    # to keep Azurite by Sillow, that everybody beats
    # and Deimos by ItsHybrid rather than by EndLevel (костыли)
    exclude = [2299, 2234]
    return [lvl for lvl in all_levels if lvl.get("id") not in exclude]


@lru_cache
def get_pos(level_name: str) -> int:
    all_levels = get_demonlist()
    level_pos = {
        lvl["name"].lower(): lvl["placement"]
        for lvl in all_levels
    }
    try:
        return level_pos[level_name.lower()]
    except KeyError:
        raise ValueError(f"Level doesn't exist: {level_name}")


@lru_cache
def get_id(level_name: str) -> str:
    all_levels = get_demonlist()
    level_pos = {
        lvl["name"].lower(): lvl["id"]
        for lvl in all_levels
    }
    try:
        return level_pos[level_name.lower()]
    except KeyError:
        raise ValueError(f"Level doesn't exist: {level_name}")


def clear_cache():
    while True:
        time.sleep(24 * 60 * 60)  # 24h

        get_demonlist.cache_clear()
        get_pos.cache_clear()
        load_file.cache_clear()

threading.Thread(
    target=clear_cache,
    daemon=True
).start()
