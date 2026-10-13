from dados.carros import criar_carros
from repositorios.carro_repositorio import CarroRepositorio


def popular_banco():
    repositorio = CarroRepositorio()

    for carro in criar_carros():
        repositorio.cadastrar(carro)

    carros = repositorio.listar()

    print(f"\nTotal de carros no banco: {len(carros)}")

    for carro in carros:
        print(
            f"{carro['fabricante']} {carro['modelo']} "
            f"({carro['ano']}) - {carro['potencia']} cv"
        )


if __name__ == "__main__":
    popular_banco()
