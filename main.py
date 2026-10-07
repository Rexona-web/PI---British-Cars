from models.catalogo import Catalogo
from dados.carros import criar_carros


# Criação do catálogo
catalogo = Catalogo()

carros = criar_carros()

for carro in carros:
    catalogo.adicionar(carro)


# Listando os carros
print("\n=========================")
print("TODOS OS CARROS")
print("=========================")

catalogo.listar()


# Busca por modelo
print("\n=========================")
print("BUSCA POR MODELO")
print("=========================")

resultado = catalogo.buscar_por_modelo("750S")

if resultado:
    resultado.exibir_dados()
else:
    print("Carro não encontrado.")


# Filtro por fabricante
print("\n=========================")
print("FILTRO POR FABRICANTE")
print("=========================")

aston_martin = catalogo.filtrar_por_fabricante("Aston Martin")

for carro in aston_martin:
    carro.exibir_dados()


# Filtro por potência
print("\n=========================")
print("FILTRO POR POTÊNCIA")
print("=========================")

carros_potentes = catalogo.filtrar_por_potencia(700)

for carro in carros_potentes:
    carro.exibir_dados()


# Filtro por ano
print("\n=========================")
print("FILTRO POR ANO")
print("=========================")

carros_novos = catalogo.filtrar_por_ano(2024)

for carro in carros_novos:
    carro.exibir_dados()


# Filtro por preço
print("\n=========================")
print("FILTRO POR PREÇO")
print("=========================")

carros_mais_baratos = catalogo.filtrar_por_preco(1500000)

for carro in carros_mais_baratos:
    carro.exibir_dados()


# Filtro por velocidade
print("\n=========================")
print("FILTRO POR VELOCIDADE")
print("=========================")

carros_rapidos = catalogo.filtrar_por_velocidade(330)

for carro in carros_rapidos:
    carro.exibir_dados()


# Remoção
print("\n=========================")
print("REMOÇÃO DE CARRO")
print("=========================")

removido = catalogo.remover_por_modelo("750S")

if removido:
    print("Carro removido com sucesso.")
else:
    print("Carro não encontrado.")