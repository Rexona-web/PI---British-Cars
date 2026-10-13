from banco.conexao import conectar


class CarroRepositorio:

    def cadastrar(self, carro):
        conexao = conectar()

        try:
            cursor = conexao.cursor()

            existente = cursor.execute(
                "SELECT id FROM carros WHERE modelo = ? AND ano = ?",
                (carro.modelo, carro.ano)
            ).fetchone()

            if existente:
                return existente["id"]

            fabricante = cursor.execute(
                "SELECT id FROM fabricantes WHERE nome = ?",
                (carro.fabricante,)
            ).fetchone()

            if fabricante is None:
                cursor.execute(
                    "INSERT INTO fabricantes (nome) VALUES (?)",
                    (carro.fabricante,)
                )
                fabricante_id = cursor.lastrowid
            else:
                fabricante_id = fabricante["id"]

            cursor.execute(
                """
                INSERT INTO carros (
                    modelo, ano, preco, descricao,
                    imagem, cor, fabricante_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    carro.modelo, carro.ano, carro.preco,
                    carro.descricao, carro.imagem, carro.cor,
                    fabricante_id
                )
            )

            carro_id = cursor.lastrowid
            esp = carro.especificacoes

            cursor.execute(
                """
                INSERT INTO especificacoes (
                    carro_id, motor, potencia, torque,
                    cambio, tracao, aceleracao, velocidade_maxima
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    carro_id, esp.motor, esp.potencia, esp.torque,
                    esp.cambio, esp.tracao, esp.aceleracao,
                    esp.velocidade_maxima
                )
            )

            conexao.commit()
            return carro_id

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    def listar(self):
        conexao = conectar()

        try:
            return conexao.execute("""
                SELECT
                    carros.id,
                    carros.modelo,
                    carros.ano,
                    carros.preco,
                    carros.descricao,
                    carros.imagem,
                    carros.cor,
                    fabricantes.nome AS fabricante,
                    especificacoes.motor,
                    especificacoes.potencia,
                    especificacoes.torque,
                    especificacoes.cambio,
                    especificacoes.tracao,
                    especificacoes.aceleracao,
                    especificacoes.velocidade_maxima
                FROM carros
                INNER JOIN fabricantes
                    ON carros.fabricante_id = fabricantes.id
                INNER JOIN especificacoes
                    ON especificacoes.carro_id = carros.id
                ORDER BY fabricantes.nome, carros.modelo
            """).fetchall()

        finally:
            conexao.close()

    def buscar_por_id(self, carro_id):
        conexao = conectar()

        try:
            return conexao.execute("""
                SELECT
                    carros.id,
                    carros.modelo,
                    carros.ano,
                    carros.preco,
                    carros.descricao,
                    carros.imagem,
                    carros.cor,
                    fabricantes.nome AS fabricante,
                    especificacoes.motor,
                    especificacoes.potencia,
                    especificacoes.torque,
                    especificacoes.cambio,
                    especificacoes.tracao,
                    especificacoes.aceleracao,
                    especificacoes.velocidade_maxima
                FROM carros
                INNER JOIN fabricantes
                    ON carros.fabricante_id = fabricantes.id
                INNER JOIN especificacoes
                    ON especificacoes.carro_id = carros.id
                WHERE carros.id = ?
            """, (carro_id,)).fetchone()

        finally:
            conexao.close()

    def atualizar(self, carro_id, dados):
        conexao = conectar()

        try:
            cursor = conexao.cursor()

            existente = cursor.execute(
                "SELECT id FROM carros WHERE id = ?",
                (carro_id,)
            ).fetchone()

            if existente is None:
                return False

            fabricante = cursor.execute(
                "SELECT id FROM fabricantes WHERE nome = ?",
                (dados["fabricante"].strip(),)
            ).fetchone()

            if fabricante is None:
                cursor.execute(
                    "INSERT INTO fabricantes (nome) VALUES (?)",
                    (dados["fabricante"].strip(),)
                )
                fabricante_id = cursor.lastrowid
            else:
                fabricante_id = fabricante["id"]

            cursor.execute("""
                UPDATE carros
                SET modelo = ?, ano = ?, preco = ?,
                    descricao = ?, imagem = ?, cor = ?,
                    fabricante_id = ?
                WHERE id = ?
            """, (
                dados["modelo"].strip(),
                int(dados["ano"]),
                float(dados["preco"]),
                dados["descricao"].strip(),
                dados["imagem"].strip(),
                dados["cor"].strip(),
                fabricante_id,
                carro_id
            ))

            cursor.execute("""
                UPDATE especificacoes
                SET motor = ?, potencia = ?, torque = ?,
                    cambio = ?, tracao = ?, aceleracao = ?,
                    velocidade_maxima = ?
                WHERE carro_id = ?
            """, (
                dados["motor"].strip(),
                int(dados["potencia"]),
                int(dados["torque"]),
                dados["cambio"].strip(),
                dados["tracao"].strip(),
                float(dados["aceleracao"]),
                int(dados["velocidade_maxima"]),
                carro_id
            ))

            if cursor.rowcount == 0:
                raise ValueError(
                    "As especificações deste carro não foram encontradas."
                )

            conexao.commit()
            return True

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    def excluir(self, carro_id):
        conexao = conectar()

        try:
            cursor = conexao.execute(
                "DELETE FROM carros WHERE id = ?",
                (carro_id,)
            )

            conexao.commit()
            return cursor.rowcount > 0

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()
