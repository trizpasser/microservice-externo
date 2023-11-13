from flask import request, jsonify
from queue import Queue
from datetime import datetime, timedelta
import random

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
            "horaFinalizacao": None, 
            "valor": valor,
            "ciclista": ciclista
        }

        fila = Fila()
        fila.insere_cobranca(cobranca)

        return "Cobrança pendente registrada.", cobranca
    
    except ValueError as e:
        resposta_erro = {
            "codigo": 422,
            "mensagem": str(e)
        }
        return jsonify(resposta_erro), 422



def obtem_cobranca():
    return 1

def processa_cobrancas_atrasadas():
    return 1

class Fila():

    def __init__(self):
        self.fila_cobrancas_pendentes = Queue()

    def obtem_fila(self):
        return list(self.fila_cobrancas_pendentes.queue)
    
    def insere_cobranca(self, cobranca):
        self.fila_cobrancas_pendentes.put(cobranca)

    def obtem_e_remove_proximo_elemento(self):
        if not self.fila_cobrancas_pendentes.empty():
            proximo_elemento = self.fila_cobrancas_pendentes.get()
            return proximo_elemento
        else:
            return None  # Fila vazia
    

