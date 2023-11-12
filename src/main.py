from flask import Flask
from flask import request
from controller.EmailController import envia_email
from controller.CobrancaController import realiza_cobranca
import os

app = Flask(__name__)

@app.route('/enviarEmail', methods=['POST'])
def enviar_email_route():
    destinatario = request.form.get('destinatario')
    resultado_envio = envia_email(destinatario)
    return resultado_envio


@app.route('/cobranca', methods=['POST'])
def realizar_cobranca_route():
    valor = float(request.form.get('valor'))
    ciclista_id = int(request.form.get('ciclista_id'))
    
    resultado_cobranca = realiza_cobranca(valor, ciclista_id)
    return resultado_cobranca

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 4000)),host='0.0.0.0',debug=True)