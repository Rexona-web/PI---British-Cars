from flask import Flask, render_template

from models.catalogo import Catalogo
from dados.carros import criar_carros


app = Flask(__name__)


# Criação do catálogo
catalogo = Catalogo()

carros = criar_carros()

for carro in carros:
    catalogo.adicionar(carro)


@app.route("/")
def inicio():
    return render_template("index.html", carros=catalogo.carros)


@app.route("/carro/<modelo>")
def detalhes_carro(modelo):
    carro = catalogo.buscar_por_modelo(modelo)

    if carro is None:
        return "Carro não encontrado", 404

    return render_template("carro.html", carro=carro)


if __name__ == "__main__":
    app.run(debug=True)