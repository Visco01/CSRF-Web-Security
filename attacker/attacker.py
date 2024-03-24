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

ATTACKER_DOMAIN = "www.attacker.com:5000"

attacker_blueprint = Blueprint('attacker', __name__)

requests_log = []

@attacker_blueprint.route("/leak.html", host=ATTACKER_DOMAIN)
def leak():
    global requests_log
    requests_log = requests_log + [f"{request.method} {request.url}"]
    return render_template("leak.j2", requests_log=requests_log)


@attacker_blueprint.route("/", host=ATTACKER_DOMAIN)
def evil_index():
    return send_from_directory("evil-static", "index.html")


@attacker_blueprint.route("/<path:path>", host=ATTACKER_DOMAIN)
def evil_static(path):
    return send_from_directory("evil-static", path)
