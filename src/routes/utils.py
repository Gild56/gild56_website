from flask import g, session
from typing import Any
import os

def get_pfp(user: str) -> str:
    return g.db.get_pfp(user)

def logged_in() -> bool:
    return session.get("account_login", None) is not None

def get_username() -> str:
    return session.get("account_login", "user")

def get_role() -> str:
    return g.db.get_role(get_username())

def get_all_pfps() -> list[str]:
    return sorted(os.listdir("static/images/cubes"))

def get_len(item: list[Any] | dict[Any, Any] | tuple[Any]) -> int:
    return len(item)

def get_mean(numbers: int) -> int:
    return sum(numbers) / len(numbers)
