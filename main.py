from models.motor import Motor
from models.cor import Cor
from models.acessorio import Acessorio
from models.catalogo import Catalogo
from models.especificacoes import Especificacoes


# =========================
# CRIAÇÃO DOS CARROS
# =========================

carro1 = Motor(
    "Aston Martin Vantage",
    1500000,
    "Esportivo britânico de alto desempenho",
    "aston_martin_vantage.jpg",
    "V8 4.0 Twin-Turbo",
    665
)

carro2 = Motor(
    "McLaren 750S",
    3500000,
    "Superesportivo britânico focado em desempenho",
    "mclaren_750s.jpg",
    "V8 4.0 Twin-Turbo",
    750
)

carro3 = Cor(
    "Lotus Emira",
    950000,
    "Esportivo britânico de motor central",
    "lotus_emira.jpg",
    "Hethel Yellow",
    "Metálico"
)

carro4 = Cor(
    "Jaguar F-Type",
    800000,
    "Esportivo britânico de duas portas",
    "jaguar_f_type.jpg",
    "British Racing Green",
    "Perolizado"
)

carro5 = Acessorio(
    "Bentley Continental GT",
    1800000,
    "Grand Tourer britânico de luxo",
    "bentley_continental_gt.jpg",
    "Sistema de som Naim",
    35000
)


# =========================
# CATÁLOGO
# =========================

catalogo = Catalogo()

catalogo.adicionar_carro(carro1)
catalogo.adicionar_carro(carro2)
catalogo.adicionar_carro(carro3)
catalogo.adicionar_carro(carro4)
catalogo.adicionar_carro(carro5)


# =========================
# LISTAGEM
# =========================

print("=== CATÁLOGO DE CARROS ESPORTIVOS BRITÂNICOS ===")

catalogo.listar_carros()


# =========================
# BUSCA
# =========================

print("\n=== BUSCA DE CARRO ===")

modelo = input("Digite o modelo que deseja buscar: ")

carro_encontrado = catalogo.buscar_por_modelo(modelo)

if carro_encontrado:
    print("\nCarro encontrado:")
    carro_encontrado.exibir_dados()
else:
    print("\nCarro não encontrado.")


# =========================
# REMOÇÃO
# =========================

print("\n=== REMOVER CARRO ===")

modelo = input("Digite o modelo que deseja remover: ")

if catalogo.remover_carro(modelo):
    print("\nCarro removido com sucesso!")
else:
    print("\nCarro não encontrado.")


# =========================
# CATÁLOGO ATUALIZADO
# =========================

print("\n=== CATÁLOGO ATUALIZADO ===")

catalogo.listar_carros()