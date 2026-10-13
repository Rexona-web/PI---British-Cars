from banco.conexao import conectar


class UsuarioRepositorio:

    def buscar_por_email(self, email):
        conexao = conectar()

        try:
            return conexao.execute(
                """
                SELECT id, nome, email, senha_hash, tipo
                FROM usuarios
                WHERE email = ?
                """,
                (email.strip().lower(),)
            ).fetchone()

        finally:
            conexao.close()

    def cadastrar(self, nome, email, senha_hash):
        conexao = conectar()

        try:
            cursor = conexao.execute(
                """
                INSERT INTO usuarios (nome, email, senha_hash)
                VALUES (?, ?, ?)
                """,
                (nome.strip(), email.strip().lower(), senha_hash)
            )

            conexao.commit()
            return cursor.lastrowid

        finally:
            conexao.close()

    def buscar_por_id(self, usuario_id):
        conexao = conectar()

        try:
            return conexao.execute(
                """
                SELECT id, nome, email, tipo
                FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,)
            ).fetchone()

        finally:
            conexao.close()
