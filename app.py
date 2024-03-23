from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from user import user_repository

VULNERABLE_DOMAIN = "www.vulnerable.com:5000"
ATTACKER_DOMAIN = "www.attacker.com:5000"

app = Flask(__name__, host_matching=True, static_host=VULNERABLE_DOMAIN)
app.secret_key = "impossible_to_guess"
app.config["SESSION_COOKIE_HTTPONLY"] = True


def get_current_user():
    username = session.get("current_user")
    return user_repository.get_by_username(username)


@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())


@app.route("/", host=VULNERABLE_DOMAIN)
def index():
    return render_template("index.j2")


@app.route("/login", methods=["GET"], host=VULNERABLE_DOMAIN)
def login():
    if "current_user" in session:
        return redirect(url_for("index"))
    return render_template("login.j2")


@app.route("/login", methods=["POST"], host=VULNERABLE_DOMAIN)
def login_post():
    try:
        username = request.form["username"]
        password = request.form["password"]
        user = user_repository.get_by_username(username)
        assert user and user.password == password, "Invalid password"
        session["current_user"] = user.username
        return redirect(url_for("index"))
    except Exception as e:
        flash(e.args[0])
        return redirect(url_for("login"))


@app.route("/logout", host=VULNERABLE_DOMAIN)
def logout():
    session.pop("current_user")
    return redirect(url_for("index"))


requests_log = []


@app.route("/leak.html", host=ATTACKER_DOMAIN)
def leak():
    global requests_log
    requests_log = requests_log + [f"{request.method} {request.url}"]
    return render_template("leak.j2", requests_log=requests_log)


@app.route("/", host=ATTACKER_DOMAIN)
def evil_index():
    return send_from_directory("evil-static", "index.html")


@app.route("/<path:path>", host=ATTACKER_DOMAIN)
def evil_static(path):
    return send_from_directory("evil-static", path)
