
import os
import sqlite3
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort,
)
from werkzeug.security import generate_password_hash, check_password_hash

from banco.criar_tabelas import criar_tabelas
from models.catalogo import Catalogo
from models.carro import Carro
from models.especificacoes import Especificacoes
from dados.carros import criar_carros
from repositorios.carro_repositorio import CarroRepositorio
from repositorios.usuario_repositorio import UsuarioRepositorio


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "BRITISH_CARS_SECRET_KEY",
    "chave-local-apenas-para-desenvolvimento",
)

criar_tabelas()

repositorio_carros = CarroRepositorio()
repositorio_usuarios = UsuarioRepositorio()
catalogo = Catalogo()


def atualizar_catalogo():
    catalogo.carros.clear()

    for dados_carro in repositorio_carros.listar():
        catalogo.adicionar(dados_carro)


def carregar_carros_iniciais():
    for carro in criar_carros():
        if repositorio_carros.buscar_por_modelo(carro.modelo) is None:
            repositorio_carros.cadastrar(carro)

    atualizar_catalogo()


carregar_carros_iniciais()


def usuario_logado():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return None

    return repositorio_usuarios.buscar_por_id(usuario_id)


def exige_admin(funcao):
    @wraps(funcao)
    def wrapper(*args, **kwargs):
        usuario_id = session.get("usuario_id")

        if not usuario_id:
            flash("Faça login para acessar essa página.", "erro")
            return redirect(url_for("login"))

        usuario = repositorio_usuarios.buscar_por_id(usuario_id)

        if usuario is None or usuario["tipo"] != "admin":
            abort(403)

        return funcao(*args, **kwargs)

    return wrapper


def obter_dados_formulario():
    campos = [
        "modelo", "fabricante", "ano", "preco", "descricao",
        "imagem", "cor", "motor", "potencia", "torque",
        "cambio", "tracao", "aceleracao", "velocidade_maxima",
    ]

    return {
        campo: request.form.get(campo, "").strip()
        for campo in campos
    }


def validar_dados_carro(dados):
    campos_obrigatorios = [
        "modelo", "fabricante", "ano", "preco", "descricao",
        "cor", "motor", "potencia", "torque", "cambio",
        "tracao", "aceleracao", "velocidade_maxima",
    ]

    for campo in campos_obrigatorios:
        if not dados.get(campo):
            return False, f"O campo {campo.replace('_', ' ')} é obrigatório."

    try:
        dados["ano"] = int(dados["ano"])
        dados["preco"] = float(
            dados["preco"].replace(".", "").replace(",", ".")
        )
        dados["potencia"] = int(dados["potencia"])
        dados["torque"] = int(dados["torque"])
        dados["velocidade_maxima"] = int(dados["velocidade_maxima"])
        dados["aceleracao"] = float(dados["aceleracao"].replace(",", "."))
    except ValueError:
        return False, "Confira os campos numéricos informados."

    if not 1886 <= dados["ano"] <= 2100:
        return False, "Informe um ano válido."

    if (
        dados["preco"] < 0
        or dados["potencia"] <= 0
        or dados["torque"] <= 0
        or dados["velocidade_maxima"] <= 0
        or dados["aceleracao"] < 0
    ):
        return False, "Os valores numéricos informados são inválidos."

    return True, ""


def criar_objeto_carro(dados):
    especificacoes = Especificacoes(
        motor=dados["motor"],
        potencia=dados["potencia"],
        torque=dados["torque"],
        cambio=dados["cambio"],
        tracao=dados["tracao"],
        aceleracao=dados["aceleracao"],
        velocidade_maxima=dados["velocidade_maxima"],
    )

    return Carro(
        modelo=dados["modelo"],
        preco=dados["preco"],
        descricao=dados["descricao"],
        imagem=dados.get("imagem", ""),
        fabricante=dados["fabricante"],
        ano=dados["ano"],
        cor=dados["cor"],
        especificacoes=especificacoes,
    )


@app.context_processor
def disponibilizar_usuario():
    return {"usuario_atual": usuario_logado()}


@app.route("/")
def inicio():
    atualizar_catalogo()
    return render_template("index.html", carros=catalogo.carros)


@app.route("/carro/<modelo>")
def detalhes_carro(modelo):
    carro = repositorio_carros.buscar_por_modelo(modelo)

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

        try:
            repositorio_usuarios.cadastrar(
                nome=nome,
                email=email,
                senha_hash=generate_password_hash(senha),
            )
        except sqlite3.IntegrityError:
            flash("Este e-mail já está cadastrado.", "erro")
            return render_template("cadastro.html")

        flash("Cadastro realizado! Agora faça login.", "sucesso")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = repositorio_usuarios.buscar_por_email(email)

        if usuario and check_password_hash(usuario["senha_hash"], senha):
            session.clear()
            session["usuario_id"] = usuario["id"]
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
@exige_admin
def admin_carros():
    carros = repositorio_carros.listar()
    return render_template("admin_carros.html", carros=carros)


@app.route("/admin/carros/novo", methods=["GET", "POST"])
@exige_admin
def novo_carro():
    if request.method == "POST":
        dados = obter_dados_formulario()
        valido, mensagem = validar_dados_carro(dados)

        if not valido:
            flash(mensagem, "erro")
            return render_template(
                "admin_formulario.html", carro=dados, titulo="Cadastrar carro"
            )

        try:
            repositorio_carros.cadastrar(criar_objeto_carro(dados))
        except sqlite3.IntegrityError:
            flash("Não foi possível cadastrar o carro.", "erro")
            return render_template(
                "admin_formulario.html", carro=dados, titulo="Cadastrar carro"
            )

        atualizar_catalogo()
        flash("Carro cadastrado com sucesso!", "sucesso")
        return redirect(url_for("admin_carros"))

    return render_template(
        "admin_formulario.html", carro=None, titulo="Cadastrar carro"
    )


@app.route("/admin/carros/<int:carro_id>/editar", methods=["GET", "POST"])
@exige_admin
def editar_carro(carro_id):
    carro_existente = repositorio_carros.buscar_por_id(carro_id)

    if carro_existente is None:
        abort(404)

    if request.method == "POST":
        dados = obter_dados_formulario()
        valido, mensagem = validar_dados_carro(dados)

        if not valido:
            flash(mensagem, "erro")
            return render_template(
                "admin_formulario.html", carro=dados, titulo="Editar carro"
            )

        try:
            repositorio_carros.atualizar(
                carro_id, criar_objeto_carro(dados)
            )
        except sqlite3.IntegrityError:
            flash("Não foi possível atualizar o carro.", "erro")
            return render_template(
                "admin_formulario.html", carro=dados, titulo="Editar carro"
            )

        atualizar_catalogo()
        flash("Carro atualizado com sucesso!", "sucesso")
        return redirect(url_for("admin_carros"))

    return render_template(
        "admin_formulario.html",
        carro=carro_existente,
        titulo="Editar carro",
    )


@app.route("/admin/carros/<int:carro_id>/excluir", methods=["POST"])
@exige_admin
def excluir_carro(carro_id):
    if repositorio_carros.buscar_por_id(carro_id) is None:
        abort(404)

    repositorio_carros.excluir(carro_id)
    atualizar_catalogo()
    flash("Carro excluído com sucesso!", "sucesso")
    return redirect(url_for("admin_carros"))


@app.errorhandler(403)
def acesso_negado(_erro):
    return render_template("403.html"), 403


if __name__ == "__main__":
    app.run(debug=True)