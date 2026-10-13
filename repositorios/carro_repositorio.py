from banco.conexao import conectar

class CarroRepositorio:

    def cadastrar(self, carro):
        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                "SELECT id FROM fabricantes WHERE nome = ?",
                (carro.fabricante,)
            )
            fabricante = cursor.fetchone()

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
                    carro.modelo,
                    carro.ano,
                    carro.preco,
                    carro.descricao,
                    carro.imagem,
                    carro.cor,
                    fabricante_id
                )
            )

            carro_id = cursor.lastrowid
            especificacoes = carro.especificacoes

            cursor.execute(
                """
                INSERT INTO especificacoes (
                    carro_id, motor, potencia, torque,
                    cambio, tracao, aceleracao,
                    velocidade_maxima
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    carro_id,
                    especificacoes.motor,
                    especificacoes.potencia,
                    especificacoes.torque,
                    especificacoes.cambio,
                    especificacoes.tracao,
                    especificacoes.aceleracao,
                    especificacoes.velocidade_maxima
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
            return conexao.execute(
                """
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
                """
            ).fetchall()

        finally:
            conexao.close()

    def buscar_por_id(self, carro_id):
        conexao = conectar()

        try:
            return conexao.execute(
                """
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
                """,
                (carro_id,)
            ).fetchone()

        finally:
            conexao.close()

    def buscar_por_modelo(self, modelo):
        conexao = conectar()

        try:
            return conexao.execute(
                """
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
                WHERE LOWER(carros.modelo) = LOWER(?)
                """,
                (modelo,)
            ).fetchone()

        finally:
            conexao.close()

    def atualizar(self, carro_id, carro):
        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                "SELECT id FROM fabricantes WHERE nome = ?",
                (carro.fabricante,)
            )
            fabricante = cursor.fetchone()

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
                UPDATE carros
                SET modelo = ?,
                    ano = ?,
                    preco = ?,
                    descricao = ?,
                    imagem = ?,
                    cor = ?,
                    fabricante_id = ?
                WHERE id = ?
                """,
                (
                    carro.modelo,
                    carro.ano,
                    carro.preco,
                    carro.descricao,
                    carro.imagem,
                    carro.cor,
                    fabricante_id,
                    carro_id
                )
            )

            if cursor.rowcount == 0:
                raise ValueError("Carro não encontrado.")

            especificacoes = carro.especificacoes

            cursor.execute(
                """
                UPDATE especificacoes
                SET motor = ?,
                    potencia = ?,
                    torque = ?,
                    cambio = ?,
                    tracao = ?,
                    aceleracao = ?,
                    velocidade_maxima = ?
                WHERE carro_id = ?
                """,
                (
                    especificacoes.motor,
                    especificacoes.potencia,
                    especificacoes.torque,
                    especificacoes.cambio,
                    especificacoes.tracao,
                    especificacoes.aceleracao,
                    especificacoes.velocidade_maxima,
                    carro_id
                )
            )

            if cursor.rowcount == 0:
                cursor.execute(
                    """
                    INSERT INTO especificacoes (
                        carro_id, motor, potencia, torque,
                        cambio, tracao, aceleracao,
                        velocidade_maxima
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        carro_id,
                        especificacoes.motor,
                        especificacoes.potencia,
                        especificacoes.torque,
                        especificacoes.cambio,
                        especificacoes.tracao,
                        especificacoes.aceleracao,
                        especificacoes.velocidade_maxima
                    )
                )

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    def excluir(self, carro_id):
        conexao = conectar()

        try:
            cursor = conexao.cursor()

            cursor.execute(
                "DELETE FROM carros WHERE id = ?",
                (carro_id,)
            )

            if cursor.rowcount == 0:
                raise ValueError("Carro não encontrado.")

            conexao.commit()

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()