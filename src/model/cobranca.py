class Cobranca:
    def __init__(self, id : int, ciclista : str, status : str, hora_solicitacao: str, hora_finalizacao : str, valor : float):
        self.id = id
        self.ciclista = ciclista
        self.status = status
        self.hora_solicitacao = hora_solicitacao
        self.hora_finalizacao = hora_finalizacao
        self.valor = valor