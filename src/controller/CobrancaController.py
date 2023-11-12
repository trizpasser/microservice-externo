from flask import request 
from flask import jsonify
from datetime import datetime
from datetime import timedelta
import random

def realiza_cobranca(valor, ciclista_id):
    if valor is None or ciclista_id is None:
        resposta_erro = {

            "codigo": 400,
            "mensagem": "Valores inválidos foram fornecidos."
        }
        return jsonify(resposta_erro), 400
    
    try: 
        if valor <= 0 or ciclista_id <= 0:
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
            "ciclista": ciclista_id
        }

        return jsonify(resposta), 200

    except ValueError as e:
        # Caso dê erro deve ser add à lista de cobranças pendentes
        resposta_erro = {
            "codigo": 422,
            "mensagem": str(e)
        }
        return jsonify(resposta_erro), 422

