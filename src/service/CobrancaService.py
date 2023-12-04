from queue import Queue
from datetime import datetime, timedelta
from flask import jsonify
from enum import Enum
from dotenv import load_dotenv
from schedule import repeat, every
import os, sys, random, stripe, schedule, time, threading, requests

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from model.cobranca import Cobranca
from model.cartao_credito import CartoDeCredito

class CobrancaService: 
    load_dotenv()

    def __init__(self):
        #self.public_key = "pk_test_51OHrHLFrYaHOdlTY1ZVqHGiHLIyGQjiKLlF1BMKOd9VFU99rKxO5JXU2bExGCMk8UDNZsteFsJBlXr5aLT110Bl100beNiidIT"
        self.api_key = os.getenv('STRIPE_PRIVATE_KEY')
        self.contador = 0

        self.thread_agendamento = threading.Thread(target=self.agendamento)
        self.thread_agendamento.daemon = True  # Define a thread como um daemon para que ela seja encerrada quando o programa principal terminar
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

        cartao = self.obtem_dados_cartao(cobranca.ciclista)

        try: 
            stripe.PaymentIntent.create(
                amount = cobranca.valor,
                currency = 'brl',
                payment_method="pm_card_visa",
            )

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
            # insere a cobrança no repository

            return info_cobranca, 200

        except Exception as e:
            self.insere_cobranca_na_fila(cobranca.valor, cobranca.ciclista)

            return jsonify({"status": "error", "mensagem": f"Erro ao realizar cobrança: {str(e)}"})

        #se não for realizada:
        #cobranca.status = Status.FALHA
        #info_cobranca = {
        #    "status": cobranca.status.value,
        #    "horaSolicitacao": cobranca.hora_solicitacao,
        #    "valor": cobranca.valor,
        #    "ciclista": cobranca.ciclista
        #}
        #insere_cobranca_na_fila(cobranca.valor, cobranca.ciclista)
        # return info_cobranca, 500
    
    def obtem_dados_cartao(self, ciclista):


        #url_dados_cartao = "https://microservice-aluguel-hm535ksnoq-uc.a.run.app/CartaoDeCredito/{ciclista}"

       #try:
        #    response = requests.get(url_dados_cartao)

            # Verifica se a requisição foi bem-sucedida (status code 2xx)
        #    if response.ok:
                # A resposta do microsserviço de destino está em response.text ou response.json()
         #       resultado = response.json()
          #      return response
          #  else:
           #     return jsonify({"status": "error", "mensagem": f"Falha na requisição: {str(e)}"})

        #except Exception as e:
         #   return jsonify ({"status": "error", "mensagem": f"Erro na requisição: {str(e)}"})
        
        return 0
    
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
        #    "id": cobranca.id,
            "status": cobranca.status.value,
        #    "horaSolicitacao": cobranca.hora_solicitacao,
        #    "horaFinalizacao": "-", 
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

                self.realiza_cobranca(valor, ciclista)
                
            return "Todas as cobrancas foram quitadas!", 200


    def obtem_cobranca(self, id_cobranca):
        cobrancas = self.lista_cobrancas()
        for cobranca in cobrancas: # cobranças no repository
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
        

    def agendamento(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    @repeat(every(5).seconds)
    def agendamento_teste():
        return requests.get("http://127.0.0.1:8080")
        #url_email = "https://microservice-externo-b4i7jmshsa-uc.a.run.app/enviarEmail"
        #dados = {"destinatario": "bqueiroz@edu.unirio.br", 
        #         "assunto": "Teste de Integração 1", 
        #         "mensagem": "teste teste teste"
        #         }
        
        #return requests.post(url_email, json = dados)

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


