from flask import Flask, request
import os, sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from service.EmailService import envia_email
from service.CobrancaService import realiza_cobranca, insere_cobranca_na_fila, processa_cobrancas_atrasadas, obtem_cobranca

app = Flask(__name__)

#cobranca_service = Cobranca()

@app.route('/enviarEmail', methods=['POST'])
def enviar_email_route():
    destinatario = request.form.get('destinatario')
    
    resultado_envio = envia_email(destinatario)
    return resultado_envio

@app.route('/cobranca', methods=['POST'])
def realizar_cobranca_route():
    valor = float(request.form.get('valor'))
    ciclista = (request.form.get('ciclista')) 
    
    resultado_cobranca = realiza_cobranca(valor, ciclista)
    return resultado_cobranca

@app.route('/processaCobrancasEmFila', methods=['POST'])
def processar_cobranca_em_fila_route():    
    
    resultado_processamento = processa_cobrancas_atrasadas()
    return resultado_processamento

@app.route('/filaCobranca', methods=['POST'])
def inserir_cobranca_em_fila_route():
    valor = float(request.form.get('valor'))
    ciclista = (request.form.get('ciclista'))
    
    resultado_insercao = insere_cobranca_na_fila(valor, ciclista)
    return resultado_insercao

@app.route('/cobranca/<int:idCobranca>', methods=['GET'])
def obter_cobranca_route(idCobranca):

    resultado_obtencao: obtem_cobranca(idCobranca)
    return resultado_obtencao


@app.route('/validaCartaoDeCredito', methods=['POST'])
def validar_cartao_de_credito_route():

    return 1

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 4000)),host='0.0.0.0',debug=True)

