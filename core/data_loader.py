import urllib.request
from typing import Any
import requests
import json
import os
from functools import lru_cache


def load_list_from_py(variable_name: str, file_name: str) -> Any:
    try:
        with open(f"..\\gild56_website_lists\\{file_name}", "r", encoding="utf-8") as f:
            code = f.read()
    except:
        with urllib.request.urlopen(f"https://raw.githubusercontent.com/Gild56/gild56_website_lists/main/{file_name}") as response:
            code = response.read().decode('utf-8')
    namespace: dict[str, Any] = {}
    exec(code, namespace)
    return namespace[variable_name]


def get_leaderboard_db() -> Any:
    local_path = "..\\gild56_website_lists\\leaderboard.json"
    url = "https://raw.githubusercontent.com/Gild56/gild56_website_lists/main/leaderboard.json"

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
