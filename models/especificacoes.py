
class Especificacoes:
    def __init__(
        self,
        motor,
        potencia,
        torque,
        cambio,
        tracao,
        aceleracao,
        velocidade_maxima
    ):
        self.__motor = motor
        self.__potencia = potencia
        self.__torque = torque
        self.__cambio = cambio
        self.__tracao = tracao
        self.__aceleracao = aceleracao
        self.__velocidade_maxima = velocidade_maxima

    @property
    def motor(self):
        return self.__motor

    @property
    def potencia(self):
        return self.__potencia

    @property
    def torque(self):
        return self.__torque

    @property
    def cambio(self):
        return self.__cambio

    @property
    def tracao(self):
        return self.__tracao

    @property
    def aceleracao(self):
        return self.__aceleracao

    @property
    def velocidade_maxima(self):
        return self.__velocidade_maxima
