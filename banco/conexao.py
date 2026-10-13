
import os
import sqlite3
from pathlib import Path


CAMINHO_BANCO = Path(__file__).resolve().parent / "british_cars.db"


def conectar(caminho=None):
    if caminho is not None:
        caminho_banco = caminho
    else:
        caminho_configurado = os.environ.get("BRITISH_CARS_DB")
        caminho_banco = (
            caminho_configurado
            if caminho_configurado
            else CAMINHO_BANCO
        )

    conexao = sqlite3.connect(caminho_banco)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")

    return conexao