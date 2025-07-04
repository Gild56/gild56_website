import os

from flask import Flask, render_template, redirect, url_for, g
from flask import session, request

from core.dbscripts import DBScripts

from static.lists.lists import get_levels_list_top, get_challenges_list_top
from static.lists.lists import get_players, get_top_players, get_top_challenge_players

app = Flask(
    __name__, static_folder="static",
    template_folder="templates"
)

with open("secret.key", "rb") as key_file:
    key = key_file.read()

app.secret_key = key


# Static pages

@app.route("/")
def index():
    return render_template(
        "index.html", logged_in=logged_in(),
        username=get_username()
    )


@app.route("/contact")
def contact():
    return render_template(
        "contact.html", logged_in=logged_in(),
        username=get_username()
    )


@app.route("/hall_of_fame")
def hall_of_fame():
    return render_template(
        "hall_of_fame.html", logged_in=logged_in(),
        username=get_username()
    )


@app.route("/games")
def games():
    return render_template(
        "games.html", logged_in=logged_in(),
        username=get_username()
    )


@app.route("/jaime_les_ours")
def jaime_les_ours():
    return render_template("jaime_les_ours.html")


# Error page

@app.route("/404")
def error404():
    return render_template(
        "404.html", logged_in=logged_in(),
        username=get_username()
    )


@app.errorhandler(404)
def handle_404(error):
    return redirect(url_for('error404'))


# Functions


def get_pfp(user) -> str:
    return g.db.get_pfp(user)


def logged_in() -> bool:
    return session.get("account_login", None) is not None


def get_username() -> str | None:
    return session.get("account_login", None)


def get_role() -> str:
    try:
        return g.db.get_role(get_username())
    except Exception:
        return "user"


def get_all_pfps() -> list:
    return sorted(os.listdir("static/images/cubes"))


# Database functions

@app.before_request
def before_request() -> None:
    if not hasattr(g, 'db'):
        g.db = DBScripts(db_name="site.db")
        g.db.connect()
        g.db.create_tables()


@app.teardown_appcontext
def teardown_request(exception=None) -> None:
    db = getattr(g, 'db', None)
    if db is not None:
        db.disconnect()
        g.pop('db', None)


# Function pages


@app.route("/delete_post/<post_id>")
def delete_post(post_id):
    print(f"delete_post({post_id})")
    if (
        get_role() == "admin"
        or get_username() == g.db.get_post_author(post_id)
    ):

        g.db.delete_post(post_id)

    return redirect(request.referrer)


@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    if (
        get_role() == "admin"
        or get_username() == g.db.get_comment_author(comment_id)
    ):

        g.db.delete_comment(comment_id)

    return redirect(request.referrer)


@app.route("/delete_user/<profile>")
def delete_user(profile):
    if (
        get_role() == "admin"
        or get_username() == g.db.get_comment_author(profile)
    ):

        g.db.delete_user(profile)

    if get_username() == g.db.get_comment_author(profile):
        session.clear()

    return redirect(url_for("community"))


@app.route("/change_role/<profile>")
def change_role(profile):
    if not get_role() == "admin":
        return

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


# Dynamic pages

@app.route("/community", methods=["GET", "POST"])
def community():
    if request.method == "POST":
        textarea_content = request.form.get("input_post_text", None)
        if textarea_content is not None:
            g.db.add_post(textarea_content, get_username())

        return redirect(url_for('community'))

    posts = g.db.get_posts()
    comments = g.db.get_comments()
    users_count = len(g.db.get_users())
    posts_count = len(posts)
    comments_count = len(comments)
    posts_and_comments_count = posts_count + comments_count

    comments_post_ids = []
    for comment in comments:
        if comment[2] in comments_post_ids:
            continue
        comments_post_ids.append(comment[2])

    print(get_pfp("sosiska17"))

    return render_template(
        "community.html", posts=posts, logged_in=logged_in(),
        username=get_username(), role=get_role(),
        posts_and_comments_count=posts_and_comments_count,
        users_count=users_count, comments=comments,
        comments_post_ids=comments_post_ids, get_pfp=get_pfp,
        get_comment_author=g.db.get_comment_author,
        get_post_author=g.db.get_post_author
    )


@app.route("/posts/<post_id>", methods=["GET", "POST"])
def post(post_id):
    if not logged_in():
        return redirect(request.referrer)

    if request.method == "POST":
        textarea_content = request.form.get("input_comment_text", None)
        if textarea_content is not None:
            print(textarea_content)
            g.db.add_comment(textarea_content, post_id, get_username())

        return redirect(url_for('post', post_id=post_id))

    return render_template(
        "post.html", post=g.db.get_post(post_id), logged_in=logged_in(),
        username=get_username(), role=get_role(), comments=g.db.get_comments(),
        get_pfp=get_pfp, get_comment_author=g.db.get_comment_author,
        get_post_author=g.db.get_post_author
    )


@app.route('/users/<profile>', methods=["GET", "POST"])
def user_profile(profile):
    if request.method == "POST":
        content = request.form["input_bio"]
        if content is not None:
            g.db.set_bio(get_username(), content)
        return redirect(url_for('user_profile', profile=profile))

    posts = g.db.get_posts()
    comments = g.db.get_comments()
    bio = g.db.get_bio(profile)

    posts_count = 0
    for post in posts:
        if post[2] == profile:
            posts_count += 1

    comments_post_ids = []
    for comment in comments:
        if comment[2] not in comments_post_ids:
            comments_post_ids.append(comment[2])

    posts_authors = []
    for post in posts:
        if post[2] not in posts_authors:
            posts_authors.append(post[2])

    theres_posts = False
    if profile in posts_authors:
        theres_posts = True

    if profile == get_username():
        my_profile = True
    else:
        my_profile = False
    if not g.db.user_exists(profile):
        return redirect(url_for('error404'))

    return render_template(
        'profile.html', username=get_username(),
        logged_in=logged_in(), my_profile=my_profile,
        posts=posts, comments=comments, profile=profile,
        comments_post_ids=comments_post_ids, bio=bio,
        get_pfp=get_pfp, profile_role=g.db.get_role(profile),
        theres_posts=theres_posts, posts_count=posts_count,
        get_role=g.db.get_role, role=get_role(),
        get_comment_author=g.db.get_comment_author,
        get_post_author=g.db.get_post_author,
        pfps=get_all_pfps()
    )


@app.route('/change_pfp', methods=['GET', 'POST'])
def change_pfp():
    if request.method == "POST":
        selected_pfp = request.form.get('selected_pfp')
        g.db.set_pfp(get_username(), selected_pfp)

        return redirect(url_for('user_profile', profile=get_username()))

    elif logged_in():
        pfps = get_all_pfps()

        return render_template(
            'change_pfp.html', username=get_username(),
            logged_in=logged_in(), pfps=pfps,
            pfps_count=len(pfps)
        )

    else:
        return redirect(url_for('log_in'))


# Lists

@app.route("/lists/levels")
def levels_list():
    return render_template(
        "list.html", logged_in=logged_in(),
        username=get_username(), levels=get_levels_list_top(),
        top="levels"
    )


@app.route("/lists/levels/<level>")
def level_page(level):
    try:
        levels_list_top = get_levels_list_top()
        index = next(i for i, item in enumerate(levels_list_top) if item[0] == level)
        level_info = levels_list_top[index]

        return render_template(
            "level.html",
            logged_in=logged_in(),
            username=get_username(),
            level=level_info,
            level_position=index + 1
        )
    except StopIteration:
        return redirect(url_for('error404'))


@app.route("/lists/challenges")
def challenges_list():
    return render_template(
        "list.html", logged_in=logged_in(),
        username=get_username(), levels=get_challenges_list_top(),
        top="challenges"
    )


@app.route("/lists/challenges/<challenge>")
def challenge_page(challenge):
    try:
        challenges_list_top = get_challenges_list_top()
        index = next(i for i, item in enumerate(challenges_list_top) if item[0] == challenge)
        level_info = challenges_list_top[index]

        return render_template(
            "level.html",
            logged_in=logged_in(),
            username=get_username(),
            level=level_info,
            level_position=index + 1
        )
    except Exception:
        return redirect(url_for('error404'))


@app.route("/lists/leaderboard")
def leaderboard():
    return render_template(
        "leaderboard.html",
        logged_in=logged_in(),
        username=get_username(),
        players=get_top_players(),
        top="levels"
    )


@app.route("/lists/challenges_leaderboards")
def challenges_leaderboard():
    return render_template(
        "leaderboard.html",
        logged_in=logged_in(),
        username=get_username(),
        players=get_top_challenge_players(),
        top="challenges"
    )


@app.route("/players/<player>")
def player_page(player):
    try:
        def get_level_rank(level_name, top_list):
            level_name = level_name.strip().lower()
            for i, level_data in enumerate(top_list):
                name = level_data[0].strip().lower()
                if name == level_name:
                    return i + 1

        top_players = get_top_players()
        top_challenge_players = get_top_challenge_players()

        levels_top_place = next(i for i, item in enumerate(top_players) if item[0] == player)
        challenges_top_place = next(i for i, item in enumerate(top_challenge_players) if item[0] == player)
        player = top_players[levels_top_place]
        challenges_profile = top_challenge_players[challenges_top_place]
        challenges_points = challenges_profile[4]

        return render_template(
            "player.html",
            logged_in=logged_in(),
            username=get_username(),
            player=player,
            challenges_points=challenges_points,
            levels_position=levels_top_place+1,
            challenges_position=challenges_top_place+1,
            challenges_list_top=get_challenges_list_top(),
            levels_list_top=get_levels_list_top(),
            get_level_rank=get_level_rank
        )
    except StopIteration:
        return redirect(url_for('error404'))


app.run(debug=True)
# app.run(host="0.0.0.0", port=5000)
