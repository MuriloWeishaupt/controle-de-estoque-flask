import sqlite3

def criar_banco():
    con = sqlite3.connect("form_db.db")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS usuarios")
    cur.execute("DROP TABLE IF EXISTS produtos")


    cur.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL)''')


    cur.execute('''CREATE TABLE IF NOT EXISTS produtos (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NOME TEXT,
                    QUANTIDADE_ESTOQUE INTEGER,
                    FABRICANTE TEXT,
                    DESCRICAO TEXT,
                    PRECO REAL)''')
    
    cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", ("admin", "admin@gmail.com", "admin"))

    con.commit()
    con.close()

criar_banco()
