from .item_catalogo import ItemCatalogo


class Motor(ItemCatalogo):
    def __init__(
        self,
        modelo,
        preco,
        descricao,
        imagem,
        especificacoes,
        tipo_motor,
        potencia
    ):
        super().__init__(
            modelo,
            preco,
            descricao,
            imagem,
            especificacoes
        )

        self.tipo_motor = tipo_motor
        self.potencia = potencia

    def exibir_dados(self):
        super().exibir_dados()
        print(f"Motor: {self.tipo_motor}")
        print(f"Potência: {self.potencia} cv")