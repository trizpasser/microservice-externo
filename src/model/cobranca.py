import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

class Cobranca:
    def __init__(self, id, ciclista, status, hora_solicitacao, hora_finalizacao, valor):
        self.id = id
        self.ciclista = ciclista
        self.status = status
        self.hora_solicitacao = hora_solicitacao
        self.hora_finalizacao = hora_finalizacao
        self.valor = valor