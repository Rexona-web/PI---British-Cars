
from dados.carros import criar_carros
from repositorios.carro_repositorio import CarroRepositorio


def popular_banco():
    repositorio = CarroRepositorio()
    carros = criar_carros()

    for carro in carros:
        repositorio.cadastrar(carro)

    cadastrados = repositorio.listar()
    print(f"Total de carros no banco: {len(cadastrados)}")

    for carro in cadastrados:
        print(
            f"{carro['fabricante']} {carro['modelo']} "
            f"({carro['ano']}) - {carro['potencia']} cv"
        )


if __name__ == "__main__":
    popular_banco()

