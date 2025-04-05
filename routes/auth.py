from flask import Blueprint, request, redirect, url_for, flash, render_template, session
import sqlite3 as sql

bp_auth = Blueprint("auth", __name__)

@bp_auth.route("/login", methods=["POST", "GET"])

def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        con = sql.connect("form_db.db")
        cur = con.cursor()
        cur.execute("SELECT id, nome, tipo FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        user = cur.fetchone()
        con.close()

        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["user_tipo"] = user[2]
            flash("Login realizado com sucesso!", "success")
            print(session)
            return redirect(url_for("produto.index"))
        else:
            flash("Email ou senha incorretos!", "danger")

    return render_template("login.html")

@bp_auth.route("/logout")

def logout():
    session.clear()
    flash("logout realizado com Sucesso!", "success")
    return redirect(url_for("auth.login"))
