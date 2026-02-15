from flask import Flask, render_template, redirect, url_for, request, session, g
from src.routes.utils import get_username, logged_in, get_role
from src.db.dbscripts import DBScripts


def register_function_routes(app: Flask):
    @app.before_request
    def before_request() -> None:
        if not hasattr(g, 'db'):
            g.db = DBScripts(db_name="site.db")
            g.db.connect()
            g.db.create_tables()


    @app.teardown_appcontext
    def teardown_request(exception: BaseException | None = None) -> None:
        db = getattr(g, 'db', None)
        if db is not None:
            db.disconnect()
            g.pop('db', None)

    @app.route("/delete_post/<post_id>")
    def delete_post(post_id: str):
        if (
            get_role() == "admin"
            or get_username() == g.db.get_post_author(post_id)
        ):

            g.db.delete_post(post_id)

        return redirect(request.referrer)


    @app.route("/delete_comment/<comment_id>")
    def delete_comment(comment_id: str):
        if (
            get_role() == "admin"
            or get_username() == g.db.get_comment_author(comment_id)
        ):

            g.db.delete_comment(comment_id)

        return redirect(request.referrer)


    @app.route("/delete_user/<profile>")
    def delete_user(profile: str):
        if (
            get_role() == "admin"
            or get_username() == g.db.get_comment_author(profile)
        ):

            g.db.delete_user(profile)

        if get_username() == g.db.get_comment_author(profile):
            session.clear()

        return redirect(url_for("community"))


    @app.route("/change_role/<profile>")
    def change_role(profile: str):
        if not get_role() == "admin":
            return redirect(url_for("community"))

        if g.db.get_role(profile) == "admin":
            g.db.set_role(profile, "user")
        else:
            g.db.set_role(profile, "admin")

        return redirect(url_for('user_profile', profile=profile))


    # Connextion pages

    @app.route("/log_out")
    def log_out():
        if not logged_in():
            return redirect(request.referrer)

        session.clear()
        return redirect(request.referrer)


    @app.route("/log_in", methods=["GET", "POST"])
    def log_in():
        if logged_in():
            return redirect(request.referrer)

        error_message = None

        if request.method == "POST":
            login = request.form["input_login"]
            password = request.form["input_password"]
            if g.db.check_userdata(login, password):
                session["account_login"] = login
                session["role"] = g.db.get_role(login)
                return redirect(url_for('community'))
            else:
                error_message = "Incorrect login or password!"

        return render_template(
            "log_in.html", logged_in=logged_in(),
            error_message=error_message
        )


    @app.route("/sign_up", methods=["GET", "POST"])
    def sign_up():
        if logged_in():
            return redirect(request.referrer)

        error_message = None

        if request.method == "POST":
            login = request.form["input_login"]
            password = request.form["input_password"]
            repeat_password = request.form["repeat_password"]
            email = request.form["email"]

            if g.db.user_exists(login):
                error_message = "User with this login already exists."
                return render_template(
                    "sign_up.html", logged_in=logged_in(),
                    error_message=error_message
                )

            if password != repeat_password:
                error_message = "The password isn't the same."
                return render_template(
                    "sign_up.html", logged_in=logged_in(),
                    error_message=error_message
                )

            g.db.add_user(login, password, email)
            session["account_login"] = login
            return redirect(url_for('community'))

        return render_template(
            "sign_up.html", logged_in=logged_in(),
            error_message=error_message
        )
