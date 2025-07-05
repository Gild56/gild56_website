import hashlib
from typing import final
from core.database import DataBase


@final
class DBScripts(DataBase):
    """
    # Database Scripts
    The `DBScripts` class interacts with the database.

    The list of methods:

    Create database:
    - `create_tables()`

    Add data in the db:
    - `add_user()`
    - `add_post()`
    - `add_comment()`

    Get data from the db:
    - `check_userdata()`
    - `user_exists()`
    - `get_user()`
    - `get_users()`
    - `get_role()`
    - `get_bio()`
    - `get_post()`
    - `get_posts()`
    - `get_comments()`
    - `get_post_author()`
    - `get_comment_author()`
    - `get_pfp()`

    Change data in the db:
    - `set_role()`
    - `set_bio()`
    - `set_pfp()`

    Delete data from the db:
    - `delete_user()`
    - `delete_post()`
    - `delete_comment()`

    Static methods:
    - `hash_password()`
    - `verify_password()`
    """

    def __init__(self, db_name: str):
        super().__init__(db_name=db_name)

    # Create tables

    def create_tables(self) -> None:
        """Creates tables in the database if they don't exist."""
        self.execute("create_accounts_table")
        self.execute("create_comments_table")
        self.execute("create_posts_table")

    # Static methods

    @staticmethod
    def hash_password(password: str) -> str:
        """Returns hashed password."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """Hashes the provided password and compares hashes."""
        return stored_password == (
            hashlib.sha256(provided_password.encode()).hexdigest()
        )

    # DB scripts

    def check_userdata(self, login: str, password: str) -> bool:
        """Checks if the user's login and passoword are right."""
        data = self.get_user(login)

        if not data:
            return False

        hashed_password = data[2]

        return self.verify_password(hashed_password, password)

    def user_exists(self, login: str) -> bool:
        """Checks if a user exists."""
        return self.get_user(login) is not None

    def add_user(self, login: str, password: str, email: str) -> None:
        """Adds a user with parameters and hashes his password."""
        hashed_password = self.hash_password(password)

        self.execute("add_user", [login, hashed_password, email])

        if self.connection is None:
            raise RuntimeError("Database connection is not initialized")
        self.connection.commit()

    def add_post(self, content: str, author_name: str) -> None:
        """Adds a post with parameters."""
        self.execute("add_post", [content, author_name])

    def add_comment(
            self, content: str,
            post_id: int,
            author_name: str
            ) -> None:
        """Adds a comment with parameters."""
        self.execute("add_comment", [content, post_id, author_name])

    def get_role(self, login: str) -> str | None:
        """Returns user's role."""
        data = self.get_user(login)

        if data is None:
            return None

        if len(data) <= 4:
            return None

        role = data[4]

        if role not in self.ROLES:
            role = "user"
            self.set_role(login, role)

        return role

    def get_posts(self) -> str | None:
        """Returns all the posts from newest to oldest."""
        data = self.execute("get_posts")
        if data is not None:
            return data[::-1]

    def get_post(self, post_id: int) -> str | None:
        """Returns a post by id."""
        data = self.execute("get_post", [post_id])
        if data is not None:
            return data[0]

    def get_comments(self) -> str | None:
        """Returns all the comments from oldest to newest."""
        return self.execute("get_comments")

    def get_users(self) -> str | None:
        """Returns all the users from oldest to newest."""
        return self.execute("get_users")

    def get_user(self, login: str) -> str | None:
        """Returns user's data by login."""
        return self.execute("get_user", [login], 1)

    def get_bio(self, login: str) -> str:
        """Returns user's bio by login."""
        data = self.execute("get_bio", [login], 1)
        if data is not None:
            return data[0]
        return "Error: Bio not found"

    def get_pfp(self, login: str) -> str:
        """Returns image path with the first letter of the login."""
        data = self.execute("get_user", [login], 1)
        if data is not None:
            return data[6]
        return "Default.png"

    def get_post_author(self, post_id: int) -> str:
        """Returns post's author by id."""
        data = self.execute("get_post_author", [post_id], 1)
        if data is not None:
            return data[0]
        return "Error: Author not found"

    def get_comment_author(self, comment_id: int) -> str:
        """Returns comment's author by id."""
        data = self.execute("get_comment_author", [comment_id], 1)
        if data is not None:
            return data[0]
        return "Error: Author not found"

    def set_role(self, login: str, role: str) -> None:
        """Sets role by login."""
        self.execute("set_role", [role, login])

    def set_bio(self, login: str, bio: str) -> None:
        """Sets bio by login."""
        self.execute("set_bio", [bio, login])

    def set_pfp(self, login: str, pfp: str) -> None:
        """Sets pfp by login."""
        self.execute("set_pfp", [pfp, login])

    def delete_post(self, post_id: int) -> None:
        """Deletes post by id."""
        self.execute("delete_post", [post_id])
        self.execute("delete_posts_comments", [post_id])

    def delete_comment(self, comment_id: int) -> None:
        """Deletes comment by id."""
        self.execute("delete_comment", [comment_id])

    def delete_user(self, login: str) -> None:
        """Deletes user by id."""
        self.execute("delete_user", [login])
        self.execute("delete_user_posts", [login])
        self.execute("delete_user_comments", [login])
