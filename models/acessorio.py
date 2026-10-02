from .item_catalogo import ItemCatalogo


class Acessorio(ItemCatalogo):
    def __init__(
        self,
        modelo,
        preco,
        descricao,
        imagem,
        especificacoes,
        acessorio,
        valor
    ):
        super().__init__(
            modelo,
            preco,
            descricao,
            imagem,
            especificacoes
        )

        self.acessorio = acessorio
        self.valor = valor

    def exibir_dados(self):
        super().exibir_dados()
        print(f"Acessório: {self.acessorio}")
        print(f"Valor do acessório: R$ {self.valor:,.2f}")