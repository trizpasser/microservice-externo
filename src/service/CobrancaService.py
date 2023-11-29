from queue import Queue
from datetime import datetime, timedelta
from enum import Enum
import random
import os, sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from model.cobranca import Cobranca
from model.cartao_credito import CartoDeCredito

class CobrancaService: 

    def lista_cobrancas(self): #remover antes dos testes
        lista = [
                {
                    "id": 1,
                    "ciclista": "123",
                    "status": "Pago",
                    "horaSolicitacao": "2023-11-13 02:14:39",
                    "horaFinalizacao": "2023-11-13 02:19:39",
                    "valor": 20.0
                },
                {
                    "id": 2,
                    "ciclista": "456",
                    "status": "Pago",
                    "horaSolicitacao": "2023-11-13 02:14:39",
                    "horaFinalizacao": "2023-11-13 02:19:39",
                    "valor": 35.5
                },
            ]
        

        return lista

    def realiza_cobranca(self, dados_cobranca):

        cobranca = Cobranca(
            valor = dados_cobranca['valor'], 
            ciclista = dados_cobranca['ciclista'], 
            id = None, 
            status = Status.OCUPADA, 
            hora_finalizacao = None, 
            hora_solicitacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if cobranca.valor <= 0 or cobranca.valor is None or cobranca.ciclista is None:
            erro = [
            {
                "codigo": 422,
                "mensagem": "Dados inválidos"
            }
        ]
            return erro, 422

        #realiza a cobranca

        # se a cobrança for realizada: 

        cobranca.id = random.randint(1,1000) # gera um id aleatorio
        cobranca.status = Status.PAGA
        cobranca.hora_finalizacao = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S") # adiciona 5min como simulação

        info_cobranca = {
            "id": cobranca.id,
            "status": cobranca.status.value,
            "horaSolicitacao": cobranca.hora_solicitacao,
            "horaFinalizacao": cobranca.hora_finalizacao,
            "valor": cobranca.valor,
            "ciclista": cobranca.ciclista
        }

        return info_cobranca, 200
    
        #se não for realizada:
        #status = Status.FALHA
        #chama fila
        
    # def 
        
    def processa_cobrancas_pendentes(self):

        if fila.vazia():
            return "Nenhuma cobrança na fila."
       
        else:
           # print("Há " + fila.__sizeof__ + "cobranças na fila")
            while fila.vazia() == False:
                cobranca_pendente = fila.obtem_cobranca()
            
                valor = cobranca_pendente["valor"]
                ciclista = cobranca_pendente["ciclista"]

                self.realiza_cobranca(valor, ciclista)
                
            return "Todas as cobrancas foram quitadas!", 200
        
        
    def insere_cobranca_na_fila(self, dados_cobranca):
        cobranca = Cobranca(
            valor = dados_cobranca['valor'], 
            ciclista = dados_cobranca['ciclista'], 
            id = random.randint(1,1000), 
            status = Status.PENDENTE, 
            hora_finalizacao = None, 
            hora_solicitacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if cobranca.valor <= 0 or cobranca.valor is None or cobranca.ciclista is None:
            erro = [
            {
                "codigo": 422,
                "mensagem": "Dados inválidos"
            }
        ]
            return erro, 422

        info_cobranca = {
            "id": cobranca.id,
            "status": cobranca.status.value,
            "horaSolicitacao": cobranca.hora_solicitacao,
            "horaFinalizacao": "-", 
            "valor": cobranca.valor,
            "ciclista": cobranca.ciclista
        }

        fila.insere_cobranca(info_cobranca)

        return fila.obtem_fila(), 200


    def obtem_cobranca(self, id_cobranca):
        cobrancas = self.lista_cobrancas()
        for cobranca in cobrancas:
            if cobranca['id'] == id_cobranca:
                return cobranca, 200
            else:
                return "Dados não encontrados", 400

    def valida_cartao(self, dados_cartao):
        cartao = CartoDeCredito(
            nome_titular = dados_cartao['nome_titular'], 
            numero = dados_cartao['numero'], 
            validade = dados_cartao['validade'], 
            cvv = dados_cartao['cvv'])

        if cartao.nome_titular and cartao.numero and cartao.validade and cartao.cvv: # retorno simulado do processo de conferencia do cartao 
            return "Cartão válido!", 200
        else: 
            return "Cartão inválido", 400

class Fila:

    def __init__(self):
        self.fila_cobrancas_pendentes = Queue()

    def obtem_fila(self):
        return list(self.fila_cobrancas_pendentes.queue)
    
    def insere_cobranca(self, cobranca):
        self.fila_cobrancas_pendentes.put(cobranca)

    def vazia(self):
        return self.fila_cobrancas_pendentes.empty()

    def obtem_cobranca(self):
        return self.fila_cobrancas_pendentes.get()
    
fila = Fila()

class Status(Enum):
    PENDENTE = "Pendente"
    PAGA = "Paga"
    FALHA = "Falha"
    CANCELADA = "Cancelada"
    OCUPADA = "Ocupada"



