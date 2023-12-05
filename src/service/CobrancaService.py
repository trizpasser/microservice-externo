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
from model.cartao_credito import CartaoDeCredito

class CobrancaService: 
    load_dotenv()

    def __init__(self):
        self.api_key = os.getenv('STRIPE_PRIVATE_KEY')

        self.thread_agendamento = threading.Thread(target=self.run_schedule)
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
    
    def requisita_cobranca(self, valor, ciclista):
        url_cobranca = "https://microservice-externo-b4i7jmshsa-uc.a.run.app/cobranca"
        
        dados = {
                 "valor": valor, 
                 "ciclista": "12345"
                 }
        try:
            response = requests.post(url_cobranca, json = dados)
            response.raise_for_status()

        # confere se a requisição retorna um json
        except requests.exceptions.RequestException as e:
            return (f"Erro na requisição: {e}")
    
        if response.status_code == 200:
            return jsonify({"mensagem": "Requisição bem-sucedida"})
        else:
            return jsonify({"mensagem": "Erro na requisição", "status_code": response.status_code})
        
    
    def efetua_cobranca(self, valor): 
        stripe.api_key = self.api_key
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

        cartao = CartaoDeCredito(
            nome_titular = dados_cartao['nome_titular'],
            numero = dados_cartao['numero'],
            validade = dados_cartao['validade'],
            cvv = dados_cartao['cvv'] )

        if self.efetua_cobranca(cobranca.valor): 
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
            self.insere_cobranca_na_fila(cobranca.valor, cobranca.ciclista)
            return "Falha na cobrança, tentaremos mais tarde."


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

        url_dados_cartao = "https://microservice-aluguel-hm535ksnoq-uc.a.run.app/cartaoDeCredito/" + ciclista

        try:
            response = requests.get(url_dados_cartao)

            # Verifica se a requisição foi bem-sucedida (status code 2xx)
            if response.ok:
                # A resposta do microsserviço de destino está em response.text ou response.json()
                resultado = response.json()
                return resultado
            else:
                
                return jsonify("Erro:", response.status_code)

        except Exception as e:
            return jsonify ({"status": "error", "mensagem": f"Erro na requisição: {str(e)}"})
        

    
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
        cartao = CartaoDeCredito(
            nome_titular = dados_cartao['nome_titular'], 
            numero = dados_cartao['numero'], 
            validade = dados_cartao['validade'], 
            cvv = dados_cartao['cvv'])

        if cartao.nome_titular and cartao.numero and cartao.validade and cartao.cvv: # retorno simulado do processo de conferencia do cartao 
            return "Cartão válido!", 200
        else: 
            return "Cartão inválido", 400
        

    def run_schedule(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    #@repeat(every(5).seconds)
    #def agendamento_teste():
    #    return requests.get("http://127.0.0.1:8080")
               

    def requisita_enviar_email(self, destinatario, assunto, mensagem):  #o destinatario na vdd é o meu pq é o unico que recebe, mas vc pode tirar ele como hardcode e enviar como parametro
        url_email = "https://microservice-externo-b4i7jmshsa-uc.a.run.app/enviarEmail"
        
        dados = {"destinatario": "bqueiroz@edu.unirio.br", 
                 "assunto": assunto, 
                 "mensagem": mensagem
                 }
        try:
            response = requests.post(url_email, json = dados)
            response.raise_for_status()

        # confere se a requisição retorna um json
        except requests.exceptions.RequestException as e:
            return (f"Erro na requisição: {e}")
    
        if response.status_code == 200:
            return jsonify({"mensagem": "Requisição bem-sucedida"})
        else:
            return jsonify({"mensagem": "Erro na requisição", "status_code": response.status_code})


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


