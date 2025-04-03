from flask import Blueprint, request, url_for, redirect, render_template, session, flash
import sqlite3 as sql

bp_usuario = Blueprint("usuario", __name__)

@bp_usuario.route("/adicionar_usuario", methods=["POST", "GET"])

def adicionar_usuario():
    if "user_id" not in session or session.get("user_name") != "admin":
        flash("Acesso negado!", "danger")
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        con = sql.connect("form_db.db")
        cur = con.cursor()
        cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        con.commit()
        con.close()

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("produto.index"))
    
    return render_template("add_usuario.html")