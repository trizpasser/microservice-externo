from flask import jsonify
from queue import Queue
from unittest.mock import Mock
from datetime import datetime, timedelta
import random, schedule, time, mock

requests = Mock()

def lista_cobrancas():
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

def realiza_cobranca(valor, ciclista):
    try: 
        if valor <= 0 or valor is None or ciclista is None:
            raise ValueError("Os dados fornecidos são inválidos.", 400)
        
        # supostamente rola um processo de cobrança aqui

        cobranca_id = random.randint(1,1000) # gera um id aleatorio
        status = "Pago" # estatico, considerar mudar
        hora_solicitacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hora_finalizacao = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S") # adiciona 5min como simulação

        resposta = {
            "id": cobranca_id,
            "status": status,
            "horaSolicitacao": hora_solicitacao,
            "horaFinalizacao": hora_finalizacao,
            "valor": valor,
            "ciclista": ciclista
        }

        # aqui supostamente guarda a cobrança no bd

        return jsonify(resposta), 200

    except ValueError as e:
        # Caso dê erro deve ser add à lista de cobranças pendentes
        resposta_erro = {
            "codigo": 422,
            "mensagem": str(e)
        }
        return jsonify(resposta_erro), 422
    
def insere_cobranca_na_fila(valor, ciclista):
    try: 
        if valor <= 0 or valor is None or ciclista is None:
            raise ValueError("Os dados fornecidos são inválidos.", 400)
        
        cobranca_id = random.randint(1,1000) # gera id aleatorio
        status = "Pendente"
        hora_solicitacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # hora_finalizacao = None  # Ainda não finalizada

        cobranca = {
            "id": cobranca_id,
            "status": status,
            "horaSolicitacao": hora_solicitacao,
            "horaFinalizacao": "-", 
            "valor": valor,
            "ciclista": ciclista
        }

        fila = Fila()
        fila.insere_cobranca(cobranca)

        agenda_processamento_de_cobranca

        return jsonify("Cobranca pendente registrada!", cobranca)
    
    except ValueError as e:
        resposta_erro = {
            "codigo": 422,
            "mensagem": str(e)
        }
        return jsonify(resposta_erro), 422


def processa_cobrancas_atrasadas():
    try:
        fila = Fila()

        while fila.confere_se_vazia != None:
            cobranca_pendente = fila.obtem_cobranca()
        
            valor = cobranca_pendente["valor"]
            ciclista = cobranca_pendente["ciclista"]

            realiza_cobranca(valor, ciclista)

        else: 
            return "Todas as cobrancas foram quitadas."

    except ValueError as e:
        resposta_erro = {
            "codigo": 422,
            "mensagem": str(e)
        }
        return jsonify(resposta_erro), 422

def agenda_processamento_de_cobranca():
    schedule.every().day.at("00:00").do(processa_cobrancas_atrasadas)
    schedule.every().day.at("12:00").do(processa_cobrancas_atrasadas)

    while True:
        schedule.run_pending()
        time.sleep(1)

def obtem_cobranca(idCobranca):
    cobrancas = lista_cobrancas()

    for cobranca in cobrancas:
        if cobranca['id'] == idCobranca:
            return cobranca
        
    response_mock = Mock()
    response_mock.status_code = 422
    response_mock.json.return_value = [
        {
            "codigo": 404,
            "mensagem": "Não encontrado."
        }
    ]

    return response_mock.json()

class Fila():

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

