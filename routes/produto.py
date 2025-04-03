from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3 as sql

bp_produto = Blueprint("produto",__name__)

@bp_produto.route("/")
@bp_produto.route("/index") 

def index():

    if "user_id" not in session:
        flash("Você precisa fazer login para acessar essa página")
        return  redirect(url_for("auth.login"))

    con = sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from produtos")
    data = cur.fetchall()
    return render_template("index.html", datas=data)


#Rota Adicionar Produto
@bp_produto.route("/add_produto", methods=["POST", "GET"])

def add_produto():

    if "user_id" not in session:
        flash("Você precisa fazer login para acessar essa página")
        return  redirect(url_for("auth.login"))
    
    if request.method=="POST":
        nome = request.form["nome"]
        quantidade_estoque = request.form["quantidade_estoque"]
        fabricante  =request.form["fabricante"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        con = sql.connect("form_db.db")
        cur = con.cursor()
        cur.execute("insert into produtos(NOME, QUANTIDADE_ESTOQUE, FABRICANTE, DESCRICAO, PRECO) values (?,?,?,?,?)", (nome, quantidade_estoque, fabricante, descricao, preco))
        con.commit()
        flash("Dados cadastrados!", "success")
        return redirect(url_for("produto.index"))
    return render_template("add_produto.html")


#Rota Atualzar Produto
@bp_produto.route("/edit_produto/<string:id>", methods=["POST", "GET"])

def edit_produto(id):
    if request.method == "POST":
        nome = request.form["nome"]
        quantidade_estoque = request.form["quantidade_estoque"]
        fabricante  =request.form["fabricante"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        con = sql.connect("form_db.db")
        cur = con.cursor()
        cur.execute("update produtos set NOME=?, QUANTIDADE_ESTOQUE=?, FABRICANTE=?, DESCRICAO=?, PRECO=? where ID=?", (nome, quantidade_estoque, fabricante, descricao, preco, id))
        con.commit()
        flash("Dados Atualizados!", "success")
        return redirect(url_for("produto.index"))
    con = sql.connect("form_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from produtos where ID=?", (id,))
    data= cur.fetchone()
    return render_template("edit_produto.html", data=data)

#Rota Deletar Produto

@bp_produto.route("/delete_produto/<string:id>", methods=["GET"])

def delete_produto(id):
    con = sql.connect("form_db.db")
    cur = con.cursor()
    cur.execute("delete from produtos where ID=?", (id,))
    con.commit()
    flash("Dados Deletados!", "warning")
    return redirect(url_for("produto.index"))
    