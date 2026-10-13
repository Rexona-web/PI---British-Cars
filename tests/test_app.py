
import uuid

import pytest
from werkzeug.security import generate_password_hash

from app import app, repositorio_usuarios


@pytest.fixture
def cliente():
    app.config["TESTING"] = True

    with app.test_client() as cliente:
        yield cliente


def test_pagina_inicial(cliente):
    assert cliente.get("/").status_code == 200


def test_paginas_de_cadastro_e_login(cliente):
    assert cliente.get("/cadastro").status_code == 200
    assert cliente.get("/login").status_code == 200


def test_administracao_exige_login(cliente):
    resposta = cliente.get("/admin/carros")
    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_usuario_comum_nao_acessa_administracao(cliente):
    email = f"usuario_{uuid.uuid4().hex}@example.com"

    usuario_id = repositorio_usuarios.cadastrar(
        "Usuario Teste",
        email,
        generate_password_hash("SenhaTeste123"),
    )

    with cliente.session_transaction() as sessao:
        sessao["usuario_id"] = usuario_id

    resposta = cliente.get("/admin/carros")
    assert resposta.status_code == 403


def test_cadastro_recusa_senha_curta(cliente):
    resposta = cliente.post(
        "/cadastro",
        data={
            "nome": "Teste",
            "email": f"curta_{uuid.uuid4().hex}@example.com",
            "senha": "123",
        },
        follow_redirects=True,
    )

    assert resposta.status_code == 200
    assert b"pelo menos 8 caracteres" in resposta.data


def test_cadastro_valido_redireciona_para_login(cliente):
    resposta = cliente.post(
        "/cadastro",
        data={
            "nome": "Usuario Teste",
            "email": f"cadastro_{uuid.uuid4().hex}@example.com",
            "senha": "SenhaTeste123",
        },
    )

    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_login_com_credenciais_validas(cliente):
    email = f"login_{uuid.uuid4().hex}@example.com"
    senha = "SenhaTeste123"

    repositorio_usuarios.cadastrar(
        "Usuario Login Teste",
        email,
        generate_password_hash(senha),
    )

    resposta = cliente.post(
        "/login",
        data={"email": email, "senha": senha},
    )

    assert resposta.status_code == 302

    with cliente.session_transaction() as sessao:
        assert "usuario_id" in sessao


def test_login_com_senha_incorreta(cliente):
    email = f"senha_errada_{uuid.uuid4().hex}@example.com"

    repositorio_usuarios.cadastrar(
        "Usuario Teste",
        email,
        generate_password_hash("SenhaCorreta123"),
    )

    resposta = cliente.post(
        "/login",
        data={"email": email, "senha": "SenhaErrada123"},
    )

    assert resposta.status_code == 200

    with cliente.session_transaction() as sessao:
        assert "usuario_id" not in sessao
