from .item_catalogo import ItemCatalogo


class Cor(ItemCatalogo):
    def __init__(
        self,
        modelo,
        preco,
        descricao,
        imagem,
        especificacoes,
        cor,
        acabamento
    ):
        super().__init__(
            modelo,
            preco,
            descricao,
            imagem,
            especificacoes
        )

        self.cor = cor
        self.acabamento = acabamento

    def exibir_dados(self):
        super().exibir_dados()
        print(f"Cor: {self.cor}")
        print(f"Acabamento: {self.acabamento}")