from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
@app.route("/index") 

def index():
    con = sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from produtos")
    data = cur.fetchall()
    return render_template("index.html", datas=data)


#Rota Adicionar Produto
@app.route("/add_produto", methods=["POST", "GET"])

def add_produto():
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
        return redirect(url_for("index"))
    return render_template("add_produto.html")


#Rota Atualzar Produto
@app.route("/edit_produto/<string:id>", methods=["POST", "GET"])

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
        return redirect(url_for("index"))
    con = sql.connect("form_db.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from produtos where ID=?", (id,))
    data= cur.fetchone()
    return render_template("edit_produto.html", data=data)

#Rota Deletar Produto

@app.route("/delete_produto/<string:id>", methods=["GET"])

def delete_produto(id):
    con = sql.connect("form_db.db")
    cur = con.cursor()
    cur.execute("delete from produtos where ID=?", (id,))
    con.commit()
    flash("Dados Deletados!", "warning")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.secret_key="admin123"
    app.run(debug=True)
    