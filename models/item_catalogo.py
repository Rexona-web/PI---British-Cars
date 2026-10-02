class ItemCatalogo:
    def __init__(self, modelo, preco, descricao, imagem, especificacoes):
        self.modelo = modelo
        self.preco = preco
        self.descricao = descricao
        self.imagem = imagem
        self.especificacoes = especificacoes

    def exibir_dados(self):
        print(f"Modelo: {self.modelo}")
        print(f"Preço: R$ {self.preco:,.2f}")
        print(f"Descrição: {self.descricao}")
        print(f"Imagem: {self.imagem}")