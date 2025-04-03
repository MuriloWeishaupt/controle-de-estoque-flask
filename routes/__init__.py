from flask import Flask, redirect, url_for
import os
from routes.produto import bp_produto
from routes.auth import bp_auth

def create_app():
    app = Flask(__name__, template_folder=os.path.abspath("templates"))
    app.secret_key = "admin123"

    app.register_blueprint(bp_produto)
    app.register_blueprint(bp_auth)  


    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app
