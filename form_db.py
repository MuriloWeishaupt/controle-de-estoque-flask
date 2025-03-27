import sqlite3 as sql

con = sql.connect("form_db.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS produtos")

sql = '''CREATE TABLE "produtos" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "NOME" TEXT,
    "QUANTIDADE_ESTOQUE" INTEGER,
    "FABRICANTE" TEXT,
    "DESCRICAO" TEXT,
    "PRECO" REAL
    )'''

cur.execute(sql)
con.commit()
con.close()