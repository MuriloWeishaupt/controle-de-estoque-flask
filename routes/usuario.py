from flask import Blueprint, request, url_for, redirect, render_template, session, flash
import sqlite3 as sql
from extensoes import bcrypt

bp_usuario = Blueprint("usuario", __name__)

@bp_usuario.route("/adicionar_usuario", methods=["POST", "GET"])

def adicionar_usuario():
    if "user_id" not in session or session.get("user_tipo") != "admin":
        flash("Acesso negado!", "danger")
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        senha = request.form["senha"].strip()
        senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")
        tipo = request.form.get("tipo", "comum")

        if not nome or not email or not senha:
            flash("Todos os campos devem ser preenchidos!", "danger")

        con = sql.connect("form_db.db")
        cur = con.cursor()
        cur.execute("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)", (nome, email, senha_hash, tipo))
        con.commit()
        con.close()

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("produto.index"))
    
    return render_template("add_usuario.html")