from functools import wraps
import sqlite3

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, abort
)
from werkzeug.security import generate_password_hash, check_password_hash

from models.catalogo import Catalogo
from models.carro import Carro
from models.especificacoes import Especificacoes
from dados.carros import criar_carros
from repositorios.usuario_repositorio import UsuarioRepositorio
from repositorios.carro_repositorio import CarroRepositorio


app = Flask(__name__)
app.secret_key = "british-cars-chave-provisoria-trocar"

usuarios = UsuarioRepositorio()
repositorio_carros = CarroRepositorio()
catalogo = Catalogo()


def atualizar_catalogo():
    """Carrega o catálogo a partir dos dados persistidos no banco."""
    catalogo.carros.clear()

    for item in repositorio_carros.listar():
        especificacoes = Especificacoes(
            motor=item["motor"],
            potencia=item["potencia"],
            torque=item["torque"],
            cambio=item["cambio"],
            tracao=item["tracao"],
            aceleracao=item["aceleracao"],
            velocidade_maxima=item["velocidade_maxima"],
        )

        carro = Carro(
            modelo=item["modelo"],
            fabricante=item["fabricante"],
            ano=item["ano"],
            preco=item["preco"],
            descricao=item["descricao"],
            imagem=item["imagem"],
            cor=item["cor"],
            especificacoes=especificacoes,
        )
        catalogo.adicionar(carro)


# Garante que os seis carros existentes continuem no banco.
for carro_inicial in criar_carros():
    repositorio_carros.cadastrar(carro_inicial)

atualizar_catalogo()


def administrador_requerido(funcao):
    @wraps(funcao)
    def decorada(*args, **kwargs):
        usuario_id = session.get("usuario_id")

        if not usuario_id:
            flash("Entre na sua conta para continuar.", "erro")
            return redirect(url_for("login"))

        usuario = usuarios.buscar_por_id(usuario_id)

        if usuario is None or usuario["tipo"] != "admin":
            abort(403)

        return funcao(*args, **kwargs)

    return decorada


@app.route("/")
def inicio():
    return render_template("index.html", carros=catalogo.carros)


@app.route("/carro/<modelo>")
def detalhes_carro(modelo):
    carro = catalogo.buscar_por_modelo(modelo)

    if carro is None:
        abort(404)

    return render_template("carro.html", carro=carro)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "erro")
            return render_template("cadastro.html")

        if len(senha) < 8:
            flash("A senha deve ter pelo menos 8 caracteres.", "erro")
            return render_template("cadastro.html")

        if usuarios.buscar_por_email(email):
            flash("Este e-mail já está cadastrado.", "erro")
            return render_template("cadastro.html")

        try:
            usuarios.cadastrar(
                nome, email, generate_password_hash(senha)
            )
        except sqlite3.IntegrityError:
            flash("Não foi possível cadastrar. Verifique o e-mail.", "erro")
            return render_template("cadastro.html")

        flash("Cadastro realizado! Agora você pode entrar.", "sucesso")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = usuarios.buscar_por_email(email)

        if usuario and check_password_hash(usuario["senha_hash"], senha):
            session.clear()
            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]

            flash("Login realizado com sucesso!", "sucesso")
            return redirect(url_for("inicio"))

        flash("E-mail ou senha incorretos.", "erro")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "sucesso")
    return redirect(url_for("inicio"))


@app.route("/admin/carros")
@administrador_requerido
def admin_carros():
    return render_template(
        "admin_carros.html",
        carros=repositorio_carros.listar()
    )


@app.route("/admin/carros/novo", methods=["GET", "POST"])
@administrador_requerido
def novo_carro():
    if request.method == "POST":
        dados = coletar_dados_formulario()

        erro = validar_dados(dados)
        if erro:
            flash(erro, "erro")
            return render_template(
                "admin_formulario.html", carro=dados, titulo="Novo carro"
            )

        especificacoes = criar_especificacoes(dados)
        carro = Carro(
            modelo=dados["modelo"],
            fabricante=dados["fabricante"],
            ano=int(dados["ano"]),
            preco=float(dados["preco"].replace(",", ".")),
            descricao=dados["descricao"],
            imagem=dados["imagem"],
            cor=dados["cor"],
            especificacoes=especificacoes,
        )

        try:
            repositorio_carros.cadastrar(carro)
            atualizar_catalogo()
        except sqlite3.IntegrityError:
            flash("Não foi possível cadastrar esse carro.", "erro")
            return render_template(
                "admin_formulario.html", carro=dados, titulo="Novo carro"
            )

        flash("Carro cadastrado com sucesso!", "sucesso")
        return redirect(url_for("admin_carros"))

    return render_template(
        "admin_formulario.html", carro={}, titulo="Novo carro"
    )


@app.route("/admin/carros/<int:carro_id>/editar", methods=["GET", "POST"])
@administrador_requerido
def editar_carro(carro_id):
    carro_atual = repositorio_carros.buscar_por_id(carro_id)

    if carro_atual is None:
        abort(404)

    if request.method == "POST":
        dados = coletar_dados_formulario()
        erro = validar_dados(dados)

        if erro:
            flash(erro, "erro")
            return render_template(
                "admin_formulario.html",
                carro=dados,
                titulo="Editar carro",
            )

        try:
            atualizado = repositorio_carros.atualizar(carro_id, dados)
            if not atualizado:
                abort(404)
            atualizar_catalogo()
        except (ValueError, sqlite3.IntegrityError):
            flash("Não foi possível atualizar. Confira os dados.", "erro")
            return render_template(
                "admin_formulario.html",
                carro=dados,
                titulo="Editar carro",
            )

        flash("Carro atualizado com sucesso!", "sucesso")
        return redirect(url_for("admin_carros"))

    return render_template(
        "admin_formulario.html",
        carro=dict(carro_atual),
        titulo="Editar carro",
    )


@app.route("/admin/carros/<int:carro_id>/excluir", methods=["POST"])
@administrador_requerido
def excluir_carro(carro_id):
    excluido = repositorio_carros.excluir(carro_id)

    if not excluido:
        abort(404)

    atualizar_catalogo()
    flash("Carro excluído do catálogo.", "sucesso")
    return redirect(url_for("admin_carros"))


def coletar_dados_formulario():
    campos = [
        "fabricante", "modelo", "ano", "preco", "descricao",
        "imagem", "cor", "motor", "potencia", "torque",
        "cambio", "tracao", "aceleracao", "velocidade_maxima",
    ]
    return {
        campo: request.form.get(campo, "").strip()
        for campo in campos
    }


def validar_dados(dados):
    obrigatorios = [
        "fabricante", "modelo", "ano", "preco", "descricao",
        "imagem", "cor", "motor", "potencia", "torque",
        "cambio", "tracao", "aceleracao", "velocidade_maxima",
    ]

    if any(not dados[campo] for campo in obrigatorios):
        return "Preencha todos os campos."

    try:
        ano = int(dados["ano"])
        preco = float(dados["preco"].replace(",", "."))
        potencia = int(dados["potencia"])
        torque = int(dados["torque"])
        aceleracao = float(dados["aceleracao"].replace(",", "."))
        velocidade = int(dados["velocidade_maxima"])
    except ValueError:
        return "Ano, preço e especificações numéricas devem ser válidos."

    if not 1886 <= ano <= 2100:
        return "Informe um ano válido."

    if preco < 0 or potencia < 0 or torque < 0:
        return "Preço, potência e torque não podem ser negativos."

    if aceleracao < 0 or velocidade < 0:
        return "Aceleração e velocidade não podem ser negativas."

    return None


def criar_especificacoes(dados):
    return Especificacoes(
        motor=dados["motor"],
        potencia=int(dados["potencia"]),
        torque=int(dados["torque"]),
        cambio=dados["cambio"],
        tracao=dados["tracao"],
        aceleracao=float(dados["aceleracao"].replace(",", ".")),
        velocidade_maxima=int(dados["velocidade_maxima"]),
    )


@app.errorhandler(403)
def acesso_negado(_erro):
    return "Acesso negado: esta área é exclusiva para administradores.", 403


if __name__ == "__main__":
    app.run(debug=True)
