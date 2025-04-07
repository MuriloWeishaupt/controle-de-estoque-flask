from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3 as sql

bp_produto = Blueprint("produto", __name__, url_prefix="/estoque")

@bp_produto.route("/")
@bp_produto.route("/index")

def index():
    if "user_id" not in session:
        flash("Você precisa fazer login para acessar essa página")
        return redirect(url_for("auth.login"))
    
    nome_filtro = request.args.get("nome", "").strip()
    fabricante_filtro = request.args.get("fabricante", "").strip()
    estoque_minimo_filtro = request.args.get("estoque_minimo", "").strip()

    query_inicial = "SELECT * FROM produtos WHERE 1=1"
    params = []

    if nome_filtro:
        query_inicial += " AND NOME LIKE ?"
        params.append(f"%{nome_filtro}%")

    if fabricante_filtro:
        query_inicial += " AND FABRICANTE LIKE ?"
        params.append(f"%{fabricante_filtro}%")

    if estoque_minimo_filtro.isdigit():
        query_inicial += " AND QUANTIDADE_ESTOQUE >= ?"
        params.append(int(estoque_minimo_filtro))



    with sql.connect("form_db.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute(query_inicial, params)
        data = cur.fetchall()
        

    quantidade_minima = 2
    return render_template("index.html", datas=data, quantidade_minima=quantidade_minima, nome_filtro=nome_filtro, fabricante_filtro=fabricante_filtro, estoque_minimo_filtro=estoque_minimo_filtro)

@bp_produto.route("/add_produto", methods=["POST", "GET"])
def add_produto():
    if "user_id" not in session:
        flash("Você precisa fazer login para acessar essa página")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        nome = request.form["nome"]
        try:
            quantidade_estoque = int(request.form["quantidade_estoque"])
        except ValueError:
            flash("Quantidade inválida!", "danger")
            return redirect(url_for("produto.movimentar_produto", id=id))
        fabricante = request.form["fabricante"]
        descricao = request.form["descricao"]

        if not nome or not quantidade_estoque or not fabricante or descricao is None:
            flash("Preencha todos os campos!", "warning")
            return redirect(url_for("produto.add_produto"))

        try:
            preco = float(request.form["preco"].replace(",", "."))
        except ValueError:
            flash("Preço inválido! Use ponto ou vírgula como separador", "danger")
            return redirect(url_for("produto.add_produto"))

        with sql.connect("form_db.db") as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO produtos (NOME, QUANTIDADE_ESTOQUE, FABRICANTE, DESCRICAO, PRECO) VALUES (?, ?, ?, ?, ?)",
                (nome, quantidade_estoque, fabricante, descricao, preco)
            )
            con.commit()

        flash("Dados cadastrados!", "success")
        return redirect(url_for("produto.index"))

    return render_template("add_produto.html")

@bp_produto.route("/edit_produto/<string:id>", methods=["POST", "GET"])
def edit_produto(id):
    if request.method == "POST":
        nome = request.form["nome"]
        try:
            quantidade_estoque = int(request.form["quantidade_estoque"])
        except ValueError:
            flash("Quantidade inválida!", "danger")
            return redirect(url_for("produto.edit_produto", id=id))
        fabricante = request.form["fabricante"]
        descricao = request.form["descricao"]

        if not nome or not quantidade_estoque or not fabricante or not descricao:
            flash("Preencha todos os campos!", "warning")
            return redirect(url_for("produto.edit_produto", id=id))

        try:
            preco = float(request.form["preco"].replace(",", "."))
        except ValueError:
            flash("Preço inválido! Use ponto ou vírgula como separador", "danger")
            return redirect(url_for("produto.edit_produto", id=id))

        with sql.connect("form_db.db") as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE produtos SET NOME = ?, QUANTIDADE_ESTOQUE = ?, FABRICANTE = ?, DESCRICAO = ?, PRECO = ? WHERE ID = ?",
                (nome, quantidade_estoque, fabricante, descricao, preco, id)
            )
            con.commit()

        flash("Dados Atualizados!", "success")
        return redirect(url_for("produto.index"))

    with sql.connect("form_db.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM produtos WHERE ID = ?", (id,))
        data = cur.fetchone()

    return render_template("edit_produto.html", data=data)

@bp_produto.route("/delete_produto/<string:id>", methods=["GET"])
def delete_produto(id):
    with sql.connect("form_db.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM produtos WHERE ID = ?", (id,))
        con.commit()

    flash("Dados Deletados!", "warning")
    return redirect(url_for("produto.index"))

@bp_produto.route("/movimentar/<int:id>", methods=["GET", "POST"])
def movimentar_produto(id):
    with sql.connect("form_db.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM produtos WHERE ID = ?", (id,))
        produto = cur.fetchone()

        if request.method == "POST":
            tipo_movimentacao = request.form["tipo_movimentacao"]
            quantidade = int(request.form["quantidade"])

            if quantidade <= 0:
                flash("Quantidade inválida!", "danger")
                return redirect(url_for("produto.movimentar_produto", id=id))

            if tipo_movimentacao == 'entrada':
                nova_quantidade = produto["QUANTIDADE_ESTOQUE"] + quantidade
            elif tipo_movimentacao == 'saida':
                nova_quantidade = produto["QUANTIDADE_ESTOQUE"] - quantidade
                if nova_quantidade < 0:
                    flash("Estoque insuficiente!", "danger")
                    return redirect(url_for('produto.index'))

            cur.execute(
                "UPDATE produtos SET QUANTIDADE_ESTOQUE = ? WHERE ID = ?",
                (nova_quantidade, id)
            )

            usuario_id = session.get("user_id")

            cur.execute(
                "INSERT INTO movimentacoes (produto_id, tipo_movimentacao, quantidade, usuario_id) VALUES (?, ?, ?, ?)",
                (id, tipo_movimentacao, quantidade, usuario_id)
            )
            con.commit()

            flash("Movimentação realizada com sucesso!", "success")
            return redirect(url_for("produto.index"))

    return render_template("movimentacao_produto.html", produto=produto)

@bp_produto.route("/historico/<int:id>")
def historico_produto(id):
    if "user_id" not in session:
        flash("Você precisa fazer login!")
        return redirect(url_for("auth.login"))

    with sql.connect("form_db.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()

        cur.execute("SELECT * FROM produtos WHERE ID = ?", (id,))
        produto = cur.fetchone()
        cur.execute('''
                    SELECT m.*, u.nome as nome_usuario
                    FROM movimentacoes m
                    JOIN usuarios u ON m.usuario_id = u.id
                    WHERE m.produto_id = ?
                    ORDER BY m.data DESC
                    ''', (id,))
        historico = cur.fetchall()

        cur.execute('''
                    SELECT tipo_movimentacao, DATE(data) as dia, SUM(quantidade) as total
                    FROM movimentacoes
                    WHERE produto_id = ?
                    GROUP BY dia, tipo_movimentacao
                    ORDER BY dia ASC
                    ''', (id,))
        movimentacoes_agrupadas = cur.fetchall()
        movimentacoes_agrupadas_dict = [
            {
                "dia":  row["dia"],
                "tipo_movimentacao": row["tipo_movimentacao"],
                "total": row["total"]
            } for row in movimentacoes_agrupadas
        ]

    return render_template("historico_produto.html", produto=produto, historico=historico, movimentacoes_agrupadas=movimentacoes_agrupadas_dict)
