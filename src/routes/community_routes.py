from flask import Flask, render_template, redirect, url_for, request, g
from src.routes.utils import get_username, logged_in, get_role, get_pfp, get_all_pfps


def register_community_routes(app: Flask):

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

        comments_post_ids: list[int] = []

        comments_post_ids = []
        for comment in comments:
            if comment[2] in comments_post_ids:
                continue
            comments_post_ids.append(comment[2])

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
    def post(post_id: str):
        if not logged_in():
            return redirect(request.referrer)

        if request.method == "POST":
            textarea_content = request.form.get("input_comment_text", None)
            if textarea_content is not None:
                g.db.add_comment(textarea_content, post_id, get_username())

            return redirect(url_for('post', post_id=post_id))

        return render_template(
            "post.html", post=g.db.get_post(post_id), logged_in=logged_in(),
            username=get_username(), role=get_role(), comments=g.db.get_comments(),
            get_pfp=get_pfp, get_comment_author=g.db.get_comment_author,
            get_post_author=g.db.get_post_author
        )


    @app.route('/users/<profile>', methods=["GET", "POST"])
    def user_profile(profile: str):
        if request.method == "POST":
            content = request.form["input_bio"]
            if content:
                g.db.set_bio(get_username(), content)
            return redirect(url_for('user_profile', profile=profile))

        posts = g.db.get_posts()
        comments = g.db.get_comments()
        bio = g.db.get_bio(profile)

        posts_count = 0
        for post in posts:
            if post[2] == profile:
                posts_count += 1

        comments_post_ids: list[str] = []
        for comment in comments:
            if comment[2] not in comments_post_ids:
                comments_post_ids.append(comment[2])

        posts_authors: list[str] = []
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