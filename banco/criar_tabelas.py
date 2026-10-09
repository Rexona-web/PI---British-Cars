
from banco.conexao import conectar


def criar_tabelas():
    conexao = conectar()

    try:
        conexao.executescript("""
            CREATE TABLE IF NOT EXISTS fabricantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS carros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                modelo TEXT NOT NULL,
                ano INTEGER NOT NULL,
                preco REAL NOT NULL,
                descricao TEXT,
                imagem TEXT,
                cor TEXT,
                fabricante_id INTEGER NOT NULL,
                FOREIGN KEY (fabricante_id)
                    REFERENCES fabricantes(id)
            );

            CREATE TABLE IF NOT EXISTS especificacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                carro_id INTEGER NOT NULL UNIQUE,
                motor TEXT NOT NULL,
                potencia INTEGER NOT NULL,
                torque INTEGER NOT NULL,
                cambio TEXT,
                tracao TEXT,
                aceleracao REAL,
                velocidade_maxima INTEGER,
                FOREIGN KEY (carro_id)
                    REFERENCES carros(id)
                    ON DELETE CASCADE
            );
        """)

        conexao.commit()
        print("Tabelas criadas com sucesso!")

    finally:
        conexao.close()


if __name__ == "__main__":
    criar_tabelas()