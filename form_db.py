import sqlite3

def criar_banco():
    con = sqlite3.connect("form_db.db")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS usuarios")
    cur.execute("DROP TABLE IF EXISTS produtos")
    cur.execute("DROP TABLE IF EXISTS movimentacoes")


    cur.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    tipo TEXT CHECK(tipo IN ('admin', 'comum')) NOT NULL DEFAULT 'comum')''')


    cur.execute('''CREATE TABLE IF NOT EXISTS produtos (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NOME TEXT,
                    QUANTIDADE_ESTOQUE INTEGER,
                    FABRICANTE TEXT,
                    DESCRICAO TEXT,
                    PRECO REAL)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS movimentacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER,
                    quantidade INTEGER NOT NULL,
                    tipo_movimentacao TEXT CHECK(tipo_movimentacao in ('entrada', 'saida')) NOT NULL,
                    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (produto_id) REFERENCES produtos(id)
                    )''')
    
    cur.execute("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)", ("admin", "admin@gmail.com", "admin", "admin"))

    con.commit()
    con.close()

criar_banco()
