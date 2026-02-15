import urllib.request
from typing import Any
import threading
import requests
import json
import time
import os
from functools import lru_cache
from flask import Flask


@lru_cache
def load_file(file_name: str) -> Any:
    local_path = f"..\\gild56_website_lists\\{file_name}.json"
    url = f"https://raw.githubusercontent.com/Gild56/gild56_website_lists/main/{file_name}.json"

    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            data = f.read()
    else:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")

    return json.loads(data)


@lru_cache
def get_demonlist() -> list[dict[str, Any]]:
    response = requests.get("https://api.demonlist.org/level/classic/list")
    all_levels = response.json().get("data", {}).get("levels", [])

    if not all_levels:
        print("Error: No levels found.")
        return []

    # It removes Azurite by Royen by its id in the database
    # to keep Azurite by Sillow, that everybody beats (костыли)
    return [lvl for lvl in all_levels if lvl.get("id") != 2299]


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


def clearing_cache(app: Flask):
    if not app.debug:
        threading.Thread(
            target=clear_cache,
            daemon=True
        ).start()
