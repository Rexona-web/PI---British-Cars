
from .item_catalogo import ItemCatalogo


class Carro(ItemCatalogo):
    def __init__(
        self,
        modelo,
        fabricante,
        ano,
        preco,
        descricao,
        imagem,
        cor,
        especificacoes
    ):
        super().__init__(
            modelo,
            preco,
            descricao,
            imagem,
            especificacoes
        )

        self.__fabricante = fabricante
        self.__ano = ano
        self.__cor = cor

    @property
    def fabricante(self):
        return self.__fabricante

    @property
    def ano(self):
        return self.__ano

    @property
    def cor(self):
        return self.__cor

    def exibir_dados(self):
        super().exibir_dados()

        print(f"Fabricante: {self.fabricante}")
        print(f"Ano: {self.ano}")
        print(f"Cor: {self.cor}")

        print("\nEspecificações:")
        print(f"Motor: {self.especificacoes.motor}")
        print(f"Potência: {self.especificacoes.potencia} cv")
        print(f"Torque: {self.especificacoes.torque} Nm")
        print(f"Câmbio: {self.especificacoes.cambio}")
        print(f"Tração: {self.especificacoes.tracao}")
        print(f"0-100 km/h: {self.especificacoes.aceleracao} s")
        print(
            f"Velocidade máxima: "
            f"{self.especificacoes.velocidade_maxima} km/h"
        )
