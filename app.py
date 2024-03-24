import os
from flask import Flask

VULNERABLE_DOMAIN = "www.vulnerable.com:5000"
ATTACKER_DOMAIN = "www.attacker.com:5000"

app = Flask(__name__, host_matching=True, static_host=VULNERABLE_DOMAIN)
app.secret_key = os.urandom(24)

app.config["VULNERABLE_DOMAIN"] = VULNERABLE_DOMAIN
app.config["ATTACKER_DOMAIN"] = ATTACKER_DOMAIN

# Cookie security settings
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

db_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db')
db_path = os.path.join(db_folder, 'db.sqlite')

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=db_path,
)

from .db import db
db.init_app(app)


from .vulnerable.vulnerable import vulnerable_blueprint
app.register_blueprint(vulnerable_blueprint)

from .attacker.attacker import attacker_blueprint
app.register_blueprint(attacker_blueprint)
