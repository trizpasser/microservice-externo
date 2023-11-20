from queue import Queue
from unittest.mock import Mock
from datetime import datetime, timedelta
import random

requests = Mock()
class Cobranca: 
    def lista_cobrancas(self):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = [
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
        

        return response_mock.json()

    def realiza_cobranca(self, valor, ciclista):
        response_mock = Mock()
        response_mock.status_code = "Cobrança realizada", 200

        if valor <= 0 or valor is None or ciclista is None:
            response_mock.status_code = 422
            response_mock.json.return_value = [
            {
                "codigo": 422,
                "mensagem": "Dados inválidos"
            }
        ]
            return response_mock.json()

        # supostamente rola um processo de cobrança aqui

        cobranca_id = random.randint(1,1000) # gera um id aleatorio
        status = "Pago" # estatico, considerar mudar
        hora_solicitacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hora_finalizacao = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S") # adiciona 5min como simulação

        response_mock.json.return_value = {
            "id": cobranca_id,
            "status": status,
            "horaSolicitacao": hora_solicitacao,
            "horaFinalizacao": hora_finalizacao,
            "valor": valor,
            "ciclista": ciclista
        }

        return response_mock.json()
        

        
    def processa_cobrancas_pendentes(self):
        response_mock = Mock()
        response_mock.status_code = "Cobranças pendentes processadas", 200
        
        fila = Fila()

        while fila.confere_se_vazia() != None:
            cobranca_pendente = fila.obtem_cobranca()
        
            valor = cobranca_pendente["valor"]
            ciclista = cobranca_pendente["ciclista"]

            self.realiza_cobranca(valor, ciclista)

        response_mock.json.return_value = "Todas as cobrancas foram quitadas!"
            
        return response_mock.json()
        
        
    def insere_cobranca_na_fila(self, valor, ciclista):
        response_mock = Mock()
        response_mock.status_code = "Cobrança inserida na fila", 200

        if valor <= 0 or valor is None or ciclista is None:
            response_mock.status_code = 422
            response_mock.json.return_value = [
            {
                "codigo": 422,
                "mensagem": "Dados inválidos"
            }
        ]
            return response_mock.json()
            
        cobranca_id = random.randint(1,1000) # gera id aleatorio
        status = "Pendente"
        hora_solicitacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response_mock.json.return_value = {
            "id": cobranca_id,
            "status": status,
            "horaSolicitacao": hora_solicitacao,
            "horaFinalizacao": "-", 
            "valor": valor,
            "ciclista": ciclista
        }

        fila = Fila()
        fila.insere_cobranca(response_mock.json())

        return response_mock.json()


    def obtem_cobranca(self, id_cobranca):
        cobrancas = self.lista_cobrancas()

        for cobranca in cobrancas:
            if cobranca['id'] == id_cobranca:
                return cobranca
    
        response_mock = Mock()
        response_mock.status_code = 404
        response_mock.json.return_value = [
            {
                "codigo": 404,
                "mensagem": "Não encontrado."
            }
        ]

        return response_mock.json()

class Validacao:
    def valida_cartao(self, nome_titular, numero, validade, cvv):
        response_mock = Mock()
        response_mock.status_code = "Cartão validado", 200
        response_mock.json.return_value = "Dados atualizados!"
        
        if nome_titular and numero and validade and cvv: # retorno simulado do processo de conferencia do cartao 
            return response_mock.json()

        
        response_mock.status_code = 422
        response_mock.json.return_value = [
            {
                "codigo": 422,
                "mensagem": "Dados inválido."
            }
        ]

        return response_mock.json()


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

