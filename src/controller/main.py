from flask import Flask, request
import os, sys
from unittest.mock import Mock
from flask_wtf import CSRFProtect # LIB PARA CORREÇÃO DO CSRF NO SONAR -> DOC PARA TODOS OS MICROSERVICES
from flask_wtf.csrf import generate_csrf # LIB PARA CORREÇÃO DO CSRF NO SONAR -> DOC PARA TODOS OS MICROSERVICES

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from service.EmailService import envia_email
from service.CobrancaService import realiza_cobranca, insere_cobranca_na_fila, processa_cobrancas_pendentes, obtem_cobranca, valida_cartao

app = Flask(__name__)
requests = Mock()

# config do SONAR do problema de CSRF
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config['SECRET_KEY'] = 'teste123'
#####################################

# config do SONAR do problema de CSRF
@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    return token, 200
#####################################

@app.route('/enviarEmail', methods=['POST'])
def enviar_email_route():
    email = request.form.get('email')
    assunto = request.form.get('assunto')
    mensagem = request.form.get('mensagem')

    resultado_envio = envia_email(email, assunto, mensagem)
    return resultado_envio

@app.route('/cobranca', methods=['POST'])
def realizar_cobranca_route():
    valor = float(request.form.get('valor'))
    ciclista = int(request.form.get('ciclista')) 
    
    resultado_cobranca = realiza_cobranca(valor, ciclista)
    return resultado_cobranca

@app.route('/processaCobrancasEmFila', methods=['POST'])
def processar_cobrancas_em_fila_route():    
    
    resultado_processamento = processa_cobrancas_pendentes()
    return resultado_processamento

@app.route('/filaCobranca', methods=['POST'])
def inserir_cobranca_em_fila_route():
    valor = float(request.form.get('valor'))
    ciclista = int(request.form.get('ciclista'))
    
    resultado_insercao = insere_cobranca_na_fila(valor, ciclista)
    return resultado_insercao

@app.route('/cobranca/<int:idCobranca>', methods=['GET'])
def obter_cobranca_route(idCobranca):

    resultado_obtencao = obtem_cobranca(idCobranca)
    return resultado_obtencao


@app.route('/validaCartaoDeCredito', methods=['POST'])
def validar_cartao_route():
    cartao = (request.form.get('cartao'))
    
    resultado_validacao = valida_cartao(cartao)
    return resultado_validacao

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)

