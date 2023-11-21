from queue import Queue
from datetime import datetime, timedelta
import random

class Cobranca: 

    def lista_cobrancas(self):
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

    def realiza_cobranca(self, valor, ciclista):

        if valor <= 0 or valor is None or ciclista is None:
            erro = [
            {
                "codigo": 422,
                "mensagem": "Dados inválidos"
            }
        ]
            return erro, 422

        # supostamente rola um processo de cobrança aqui

        cobranca_id = random.randint(1,1000) # gera um id aleatorio
        status = "Pago" 
        hora_solicitacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hora_finalizacao = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S") # adiciona 5min como simulação

        info_cobranca = {
            "id": cobranca_id,
            "status": status,
            "horaSolicitacao": hora_solicitacao,
            "horaFinalizacao": hora_finalizacao,
            "valor": valor,
            "ciclista": ciclista
        }

        return info_cobranca, 200
        

        
    def processa_cobrancas_pendentes(self):
        
        fila = Fila()

        while fila.confere_se_vazia() != None:
            cobranca_pendente = fila.obtem_cobranca()
        
            valor = cobranca_pendente["valor"]
            ciclista = cobranca_pendente["ciclista"]

            self.realiza_cobranca(valor, ciclista)
            
        return "Todas as cobrancas foram quitadas!", 200
        
        
    def insere_cobranca_na_fila(self, valor, ciclista):
        if valor <= 0 or valor is None or ciclista is None:
            erro = [
            {
                "codigo": 422,
                "mensagem": "Dados inválidos"
            }
        ]
            return erro, 422

        fila = Fila()

        cobranca_id = random.randint(1,1000) # gera id aleatorio
        status = "Pendente"
        hora_solicitacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        info_cobranca = {
            "id": cobranca_id,
            "status": status,
            "horaSolicitacao": hora_solicitacao,
            "horaFinalizacao": "-", 
            "valor": valor,
            "ciclista": ciclista
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

    def valida_cartao(self, nome_titular, numero, validade, cvv):
        
        if nome_titular and numero and validade and cvv: # retorno simulado do processo de conferencia do cartao 
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

    def confere_se_vazia(self):
        if self.fila_cobrancas_pendentes.empty():
            return None

    def obtem_cobranca(self):
        return self.fila_cobrancas_pendentes.get()

