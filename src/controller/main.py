from flask import Flask, request
from unittest.mock import Mock
from flask_wtf import CSRFProtect # LIB PARA CORREÇÃO DO CSRF NO SONAR -> DOC PARA TODOS OS MICROSERVICES
from flask_wtf.csrf import generate_csrf # LIB PARA CORREÇÃO DO CSRF NO SONAR -> DOC PARA TODOS OS MICROSERVICES
import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from model.email import Email
from model.cobranca import Cobranca
from service.EmailService import EmailService
from service.CobrancaService import Cobranca

app = Flask(__name__)
requests = Mock()


cobranca = Cobranca()
email = EmailService()

#config do SONAR do problema de CSRF
#csrf = CSRFProtect(app)
#csrf.init_app(app)
#app.config['SECRET_KEY'] = 'teste123'
#####################################

# config do SONAR do problema de CSRF
#@app.route('/get_csrf_token', methods=['GET'])
#def get_csrf_token():
#    token = generate_csrf()
#    return token, 200
#####################################

@app.route('/', methods=['GET'])
def hello_world():
    return "Hello World! :)"

@app.route('/enviarEmail', methods=['POST']) 
def enviar_email_route():
    data = request.json
    destinatario, assunto, mensagem = data.get('destinatario'), data.get('assunto'), data.get('mensagem')

    return email.envia_email(destinatario, assunto, mensagem)

@app.route('/cobranca', methods=['POST'])
def realizar_cobranca_route():
    data = request.json
    valor, ciclista = float(data.get('valor')), int(data.get('ciclista'))
    
    return cobranca.realiza_cobranca(valor, ciclista)


@app.route('/processaCobrancasEmFila', methods=['POST'])
def processar_cobrancas_em_fila_route():    
    
    return cobranca.processa_cobrancas_pendentes()


@app.route('/filaCobranca', methods=['POST'])
def inserir_cobranca_em_fila_route():
    data = request.json
    valor, ciclista = float(data.get('valor')), int(data.get('ciclista'))
    
    return cobranca.insere_cobranca_na_fila(valor, ciclista)


@app.route('/cobranca/<int:id_cobranca>', methods=['GET'])
def obter_cobranca_route(id_cobranca):

    return cobranca.obtem_cobranca(id_cobranca)


@app.route('/validaCartaoDeCredito', methods=['POST'])
def validar_cartao_route():
    data = request.json
    nome_titular, numero, validade, cvv = data.get('nome_titular'), data.get('numero'), data.get('validade'), data.get('cvv')
    
    return cobranca.valida_cartao(nome_titular, numero, validade, cvv)


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)

