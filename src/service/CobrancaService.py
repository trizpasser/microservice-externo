from queue import Queue
from datetime import datetime, timedelta
from flask import jsonify
from enum import Enum
from dotenv import load_dotenv
from schedule import repeat, every
import os, sys, random, stripe, schedule, time, threading, requests
from google.cloud import secretmanager
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from model.cobranca import Cobranca
from model.cartao_credito import CartaoDeCredito

class CobrancaService: 
    load_dotenv()

    def __init__(self):
        self.thread_agendamento = threading.Thread(target=self.run_schedule)
        self.thread_agendamento.daemon = True  
        self.thread_agendamento.start()
    
    
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


    def efetua_cobranca(self, valor, dados_cartao): 
        if dados_cartao.get('ok'):
            print("Dados ok")

        stripe.api_key = self.busca_secrets_keys('STRIPE_PRIVATE_KEY')
        valor = int(valor * 100) # o amount é em centavos, então converte reais em centavos
    
        try:
            stripe.PaymentIntent.create(
                amount = valor,
                currency = "brl",
                payment_method = "pm_card_visa",
            )
            return True
        
        except Exception as e:

            return False, jsonify({"status": "error", "mensagem": f"Erro ao realizar cobrança: {str(e)}"})
        

    def obtem_dados_cartao(self, ciclista):

        url_dados_cartao = "https://microservice-aluguel-hm535ksnoq-uc.a.run.app/cartaoDeCredito/" + ciclista

        try:
            response = requests.get(url_dados_cartao)

            if response.ok:
                resultado = response.json()
                return resultado
            else:
                return jsonify("Erro:", response.status_code)

        except Exception as e:
            return jsonify ({"status": "error", "mensagem": f"Erro na requisição: {str(e)}"}), response.response_status_code


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

        dados_cartao = self.obtem_dados_cartao(cobranca.ciclista)

        if self.efetua_cobranca(cobranca.valor, dados_cartao): 
            cobranca.id = random.randint(1,1000) # gera um id aleatorio
            cobranca.status = Status.PAGA
            cobranca.hora_finalizacao = (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")

            info_cobranca = {
                "-Status-": "Cobrança realizada com sucesso!",
                "id": cobranca.id,
                "status": cobranca.status.value,
                "horaSolicitacao": cobranca.hora_solicitacao,
                "horaFinalizacao": cobranca.hora_finalizacao,
                "valor": cobranca.valor,
                "ciclista": cobranca.ciclista
            }

            return info_cobranca, 200
        
        else:
            info_cobranca = {
                "valor": cobranca.valor,
                "ciclista": cobranca.ciclista 
            }

            self.insere_cobranca_na_fila(info_cobranca)
            return "Falha na cobrança, tentaremos mais tarde."

    
    def insere_cobranca_na_fila(self, dados_cobranca):
        cobranca = Cobranca(
            valor = dados_cobranca['valor'], 
            ciclista = dados_cobranca['ciclista'], 
            id = None, 
            status = Status.PENDENTE, 
            hora_finalizacao = None, 
            hora_solicitacao = None)

        if cobranca.valor <= 0 or cobranca.valor is None or cobranca.ciclista is None:
            erro = [
            {
                "codigo": 422,
                "mensagem": "Dados inválidos"
            }
        ]
            return erro, 422

        info_cobranca = {
            "status": cobranca.status.value,
            "valor": cobranca.valor,
            "ciclista": cobranca.ciclista
        }

        fila.insere_cobranca(info_cobranca)

        return fila.obtem_fila(), 200

    @repeat(every(12).hours)
    def processa_cobrancas_pendentes(self):
        if fila.vazia():
            return "Nenhuma cobrança na fila."
       
        else:
            while fila.vazia() == False:
                cobranca_pendente = fila.obtem_cobranca()
            
                valor = cobranca_pendente["valor"]
                ciclista = cobranca_pendente["ciclista"]

                info_cobranca = {
                "valor": valor,
                "ciclista": ciclista
                 }

                self.realiza_cobranca(info_cobranca)
                
            return "Todas as cobrancas foram quitadas!", 200


    def obtem_cobranca(self, id_cobranca):
        cobrancas = self.lista_cobrancas()
        for cobranca in cobrancas: 
            if cobranca['id'] == id_cobranca:
                return cobranca, 200
            else:
                return "Dados não encontrados", 400
            

    def valida_cartao(self, dados_cartao):
        if dados_cartao.get('ok'):
            print("Dados ok")

        stripe.api_key = self.busca_secrets_keys('STRIPE_PRIVATE_KEY')

        try:
            stripe.Token.create(
                card={  
                    'number': '4000056655665556',  
                    'exp_month': '12',
                    'exp_year': '2024',
                    'cvc': '123'
                }
            )
        except Exception as e:
            return jsonify ({"status": "error", "mensagem": f"Cartão inválido: {str(e)}"}), 500
        

    def run_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    def busca_secrets_keys(self, name_key):
        client = secretmanager.SecretManagerServiceClient()   
        path = f"projects/microservice-externo/secrets/{name_key}/versions/latest"
        response = client.access_secret_version(name=path)
        return response.payload.data.decode("UTF-8")

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