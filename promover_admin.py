from banco.conexao import conectar


def promover_administrador():
    email = input("Digite o e-mail da sua conta cadastrada: ").strip().lower()

    if not email or "@" not in email:
        print("E-mail inválido.")
        return

    conexao = conectar()

    try:
        usuario = conexao.execute(
            "SELECT id, nome, tipo FROM usuarios WHERE email = ?",
            (email,)
        ).fetchone()

        if usuario is None:
            print("Conta não encontrada. Cadastre-se pelo site primeiro.")
            return

        if usuario["tipo"] == "admin":
            print(f"{usuario['nome']} já é administrador.")
            return

        confirmacao = input(
            f"Promover {usuario['nome']} a administrador? (SIM para confirmar): "
        ).strip()

        if confirmacao != "SIM":
            print("Operação cancelada.")
            return

        conexao.execute(
            "UPDATE usuarios SET tipo = 'admin' WHERE id = ?",
            (usuario["id"],)
        )
        conexao.commit()

        print(f"Conta {email} promovida a administrador.")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    promover_administrador()
