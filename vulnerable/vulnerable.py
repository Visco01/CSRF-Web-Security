from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
    Blueprint,
    current_app
)
from markupsafe import escape
from .user import user_repository
from .post import post_repository, Post

VULNERABLE_DOMAIN = "www.vulnerable.com:5000"

vulnerable_blueprint = Blueprint('vulnerable', __name__)

def get_current_user():
    username = session.get("current_user")
    return user_repository.get_by_username(username)


@vulnerable_blueprint.context_processor
def inject_user():
    return dict(current_user=get_current_user())


@vulnerable_blueprint.route("/", host=VULNERABLE_DOMAIN)
def index():
    return render_template("index.j2", posts=post_repository.posts)

@vulnerable_blueprint.route("/account", host=VULNERABLE_DOMAIN)
def account():
    return render_template("account.j2")


@vulnerable_blueprint.route("/post", methods=["POST"], host=VULNERABLE_DOMAIN)
def add_post():
    title = request.form["title"]
    desc = request.form["description"]

    # UNCOMMENT TO FIX XSS VULNERABILITY
    # title = escape(request.form["title"])
    # desc = escape(request.form["description"])

    post = Post(title, desc, get_current_user())
    post_repository.add_post(post)
    return redirect(url_for("vulnerable.index"))


@vulnerable_blueprint.route("/login", methods=["GET"], host=VULNERABLE_DOMAIN)
def login():
    if "current_user" in session:
        return redirect(url_for("vulnerable.index"))
    return render_template("login.j2")


@vulnerable_blueprint.route("/login", methods=["POST"], host=VULNERABLE_DOMAIN)
def login_post():
    try:
        username = request.form["username"]
        password = request.form["password"]
        user = user_repository.get_by_username(username)
        assert user and user.password == password, "Invalid password"
        session["current_user"] = user.username
        return redirect(url_for("vulnerable.index"))
    except Exception as e:
        flash(e.args[0])
        return redirect(url_for("vulnerable.login"))


@vulnerable_blueprint.route("/logout", host=VULNERABLE_DOMAIN)
def logout():
    session.pop("current_user")
    return redirect(url_for("vulnerable.index"))


@vulnerable_blueprint.route("/change-email", methods=["POST"], host=VULNERABLE_DOMAIN)
def change_email():
    user = get_current_user()
    user.email = request.form.get('email');
    return user.email
