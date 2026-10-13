
class Catalogo:
    def __init__(self):
        self.__carros = []

    @property
    def carros(self):
        return self.__carros

    def adicionar(self, carro):
        self.__carros.append(carro)

    def listar(self):
        for carro in self.__carros:
            print("\n-------------------------")
            carro.exibir_dados()

    def buscar_por_modelo(self, modelo):
        for carro in self.__carros:
            if carro.modelo.lower() == modelo.lower():
                return carro

        return None

    def filtrar_por_fabricante(self, fabricante):
        carros_encontrados = []

        for carro in self.__carros:
            if carro.fabricante.lower() == fabricante.lower():
                carros_encontrados.append(carro)

        return carros_encontrados

    def filtrar_por_potencia(self, potencia_minima):
        carros_encontrados = []

        for carro in self.__carros:
            if carro.especificacoes.potencia >= potencia_minima:
                carros_encontrados.append(carro)

        return carros_encontrados

    def filtrar_por_ano(self, ano_minimo):
        carros_encontrados = []

        for carro in self.__carros:
            if carro.ano >= ano_minimo:
                carros_encontrados.append(carro)

        return carros_encontrados

    def filtrar_por_preco(self, preco_maximo):
        carros_encontrados = []

        for carro in self.__carros:
            if carro.preco <= preco_maximo:
                carros_encontrados.append(carro)

        return carros_encontrados

    def filtrar_por_velocidade(self, velocidade_minima):
        carros_encontrados = []

        for carro in self.__carros:
            if carro.especificacoes.velocidade_maxima >= velocidade_minima:
                carros_encontrados.append(carro)

        return carros_encontrados

    def remover(self, carro):
        if carro in self.__carros:
            self.__carros.remove(carro)
            return True

        return False

    def remover_por_modelo(self, modelo):
        carro = self.buscar_por_modelo(modelo)

        if carro:
            self.__carros.remove(carro)
            return True

        return False
