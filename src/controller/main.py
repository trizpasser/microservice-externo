from flask import Flask, request
from unittest.mock import Mock
import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from service.EmailService import EmailService
from service.CobrancaService import CobrancaService

app = Flask(__name__)
requests = Mock()

cobranca = CobrancaService()
email = EmailService()

@app.route('/', methods=['GET']) # teste 
def hello_world():
    return "Hello World :)"

@app.route('/testeEmail', methods=['POST']) # teste 
def teste_email():
    dados_email = request.json

    destinatario = dados_email['destinatario']
    assunto = dados_email['assunto']
    mensagem = dados_email['mensagem']

    return cobranca.requisita_enviar_email(destinatario, assunto, mensagem)

@app.route('/testeCobranca', methods=['POST']) # teste 
def teste_cobranca():
    dados_cobranca = request.json

    valor = dados_cobranca['valor']
    ciclista = dados_cobranca['ciclista']

    return cobranca.requisita_cobranca(valor, ciclista)

@app.route('/testeIntegracao', methods=['POST']) # teste 
def teste_integraca():
    dados_ciclista = request.json
    ciclista = dados_ciclista['ciclista']

    return cobranca.obtem_dados_cartao(ciclista)

@app.route('/enviarEmail', methods=['POST']) 
def enviar_email_route():
    dados_email = request.json

    return email.envia_email(dados_email)


@app.route('/cobranca', methods=['POST'])
def realizar_cobranca_route():
    dados_cobranca = request.json
    
    return cobranca.realiza_cobranca(dados_cobranca)


@app.route('/processaCobrancasEmFila', methods=['POST'])
def processar_cobrancas_em_fila_route():    
    
    return cobranca.processa_cobrancas_pendentes()


@app.route('/filaCobranca', methods=['POST'])
def inserir_cobranca_em_fila_route():
    dados_cobranca = request.json
    
    return cobranca.insere_cobranca_na_fila(dados_cobranca)


@app.route('/cobranca/<int:id_cobranca>', methods=['GET'])
def obter_cobranca_route(id_cobranca):

    return cobranca.obtem_cobranca(id_cobranca)


@app.route('/validaCartaoDeCredito', methods=['POST'])
def validar_cartao_route():
    dados_cartao = request.json
    
    return cobranca.valida_cartao(dados_cartao)


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)