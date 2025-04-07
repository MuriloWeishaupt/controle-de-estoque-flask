from flask import Flask, redirect, url_for
from routes.produto import bp_produto
from routes.auth import bp_auth
from routes.usuario import bp_usuario
from extensoes import bcrypt

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = "admin123"
    
    app.register_blueprint(bp_produto)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_usuario)

    bcrypt.init_app(app)

    return app


app = create_app()


@app.route("/")
def home():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)


