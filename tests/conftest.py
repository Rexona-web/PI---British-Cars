import os
import tempfile
from pathlib import Path

import pytest


_arquivo_temporario = tempfile.NamedTemporaryFile(
    suffix=".db",
    delete=False
)
CAMINHO_BANCO_TESTES = _arquivo_temporario.name
_arquivo_temporario.close()

os.environ["BRITISH_CARS_DB"] = CAMINHO_BANCO_TESTES

from banco.criar_tabelas import criar_tabelas

criar_tabelas()


@pytest.fixture(scope="session", autouse=True)
def banco_de_testes():
    yield

    os.environ.pop("BRITISH_CARS_DB", None)
    Path(CAMINHO_BANCO_TESTES).unlink(missing_ok=True)
