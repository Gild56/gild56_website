from flask import g, session
from typing import Any
import urllib.request
import json
import os
from urllib.parse import quote


def get_pfp(user: str) -> str:
    return g.db.get_pfp(user)

def logged_in() -> bool:
    return session.get("account_login", None) is not None

def get_username() -> str:
    return session.get("account_login", "user")

def get_role() -> str:
    return g.db.get_role(get_username())

def get_len(item: list[Any] | dict[Any, Any] | tuple[Any]) -> int:
    return len(item)

def get_mean(numbers: int) -> int:
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

def get_all_pfps() -> list[str]:
    url = "https://api.github.com/repos/Gild56/gild56_website_lists/contents/images/cubes"

    token = os.getenv("GITHUB_TOKEN")

    headers = {
        "User-Agent": "Gild56-Website"
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request) as response:
        files = json.load(response)

    return sorted(
        file["name"]
        for file in files
        if file["type"] == "file"
    )

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def github_request(url: str):
    headers = {
        "User-Agent": "Gild56-Website",
        "Accept": "application/vnd.github+json"
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def get_cube(player: str):
    player_name = player.removesuffix(".png")
    return f"https://raw.githubusercontent.com/Gild56/gild56_website_lists/main/images/cubes/{player_name}.png"


def get_thumbnail(level_name: str):
    return f"https://raw.githubusercontent.com/Gild56/gild56_website_lists/main/images/thumbnails/{level_name}.png"
