from flask import g, session
from typing import Any
import urllib.request
import json


def get_pfp(user: str) -> str:
    return g.db.get_pfp(user)

def logged_in() -> bool:
    return session.get("account_login", None) is not None

def get_username() -> str:
    return session.get("account_login", "user")

def get_role() -> str:
    return g.db.get_role(get_username())

def get_all_pfps() -> list[str]:
    url = "https://api.github.com/repos/Gild56/gild56_website_lists/contents/images/cubes"

    with urllib.request.urlopen(url) as response:
        files = json.load(response)

    return sorted(
        file["name"]
        for file in files
        if file["type"] == "file"
    )

def get_len(item: list[Any] | dict[Any, Any] | tuple[Any]) -> int:
    return len(item)

def get_mean(numbers: int) -> int:
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

def get_cube(player_name: str):
    return f"https://raw.githubusercontent.com/Gild56/gild56_website_lists/refs/heads/main/images/cubes/{player_name.removesuffix(".png")}.png"

def get_thumbnail(level_name: str):
    return f"https://raw.githubusercontent.com/Gild56/gild56_website_lists/refs/heads/main/images/thumbnails/{level_name}.png"
