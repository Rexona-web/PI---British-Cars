from models.carro import Carro
from models.especificacoes import Especificacoes


def criar_carros():

    # Aston Martin Vantage
    especificacoes_vantage = Especificacoes(
        "V8 4.0 Twin-Turbo",
        665,
        800,
        "Automático 8 marchas",
        "Traseira",
        3.5,
        325
    )

    carro1 = Carro(
        "Vantage",
        "Aston Martin",
        2024,
        1500000,
        "Esportivo britânico de alto desempenho.",
        "aston_martin_vantage.jpg",
        "British Racing Green",
        especificacoes_vantage
    )


    # McLaren 750S
    especificacoes_750s = Especificacoes(
        "V8 4.0 Twin-Turbo",
        750,
        800,
        "Automático 7 marchas",
        "Traseira",
        2.8,
        332
    )

    carro2 = Carro(
        "750S",
        "McLaren",
        2023,
        3500000,
        "Superesportivo britânico focado em desempenho.",
        "mclaren_750s.jpg",
        "Laranja",
        especificacoes_750s
    )


    # Aston Martin DBS
    especificacoes_dbs = Especificacoes(
        "V12 5.2 Twin-Turbo",
        715,
        900,
        "Automático 8 marchas",
        "Traseira",
        3.4,
        340
    )

    carro3 = Carro(
        "DBS",
        "Aston Martin",
        2023,
        3000000,
        "Grand tourer britânico com motor V12 e alto desempenho.",
        "aston_martin_dbs.jpg",
        "Preto",
        especificacoes_dbs
    )


    # Bentley Continental GT
    especificacoes_continental = Especificacoes(
        "W12 6.0 Twin-Turbo",
        659,
        900,
        "Automático 8 marchas",
        "Integral",
        3.6,
        335
    )

    carro4 = Carro(
        "Continental GT",
        "Bentley",
        2024,
        3200000,
        "Grand tourer britânico que combina luxo e desempenho.",
        "bentley_continental_gt.jpg",
        "Azul",
        especificacoes_continental
    )


    # Lotus Emira
    especificacoes_emira = Especificacoes(
        "V6 3.5 Supercharged",
        400,
        430,
        "Manual 6 marchas",
        "Traseira",
        4.3,
        290
    )

    carro5 = Carro(
        "Emira",
        "Lotus",
        2024,
        1000000,
        "Esportivo leve focado em dirigibilidade e desempenho.",
        "lotus_emira.jpg",
        "Amarelo",
        especificacoes_emira
    )


    # Jaguar F-Type
    especificacoes_ftype = Especificacoes(
        "V8 5.0 Supercharged",
        575,
        700,
        "Automático 8 marchas",
        "Integral",
        3.7,
        300
    )

    carro6 = Carro(
        "F-Type",
        "Jaguar",
        2024,
        1200000,
        "Esportivo britânico de alto desempenho com motor V8.",
        "jaguar_f_type.jpg",
        "Verde",
        especificacoes_ftype
    )


    return [
        carro1,
        carro2,
        carro3,
        carro4,
        carro5,
        carro6
    ]