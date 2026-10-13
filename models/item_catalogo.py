
class ItemCatalogo:
    def __init__(self, modelo, preco, descricao, imagem, especificacoes):
        self.__modelo = modelo
        self.__preco = preco
        self.__descricao = descricao
        self.__imagem = imagem
        self.__especificacoes = especificacoes

    @property
    def modelo(self):
        return self.__modelo

    @property
    def preco(self):
        return self.__preco

    @property
    def descricao(self):
        return self.__descricao

    @property
    def imagem(self):
        return self.__imagem

    @property
    def especificacoes(self):
        return self.__especificacoes

    def exibir_dados(self):
        print(f"Modelo: {self.modelo}")
        print(f"Preço: R$ {self.preco:,.2f}")
        print(f"Descrição: {self.descricao}")
        print(f"Imagem: {self.imagem}")
