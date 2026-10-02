class Catalogo:
    def __init__(self):
        self.carros = []

    def adicionar_carro(self, carro):
        self.carros.append(carro)

    def listar_carros(self):
        for carro in self.carros:
            print("\n-------------------------")
            carro.exibir_dados()

    def buscar_por_modelo(self, modelo):
        for carro in self.carros:
            if carro.modelo.lower() == modelo.lower():
                return carro

    def remover_carro(self, modelo):
        for carro in self.carros:
            if carro.modelo.lower() == modelo.lower():
                self.carros.remove(carro)
            return True

        return False