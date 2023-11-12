from flask import Flask
import os
from controller.EmailController import envia_email

app = Flask(__name__)

@app.route('/enviarEmail', methods=['POST'])
def enviar_email_route():
    resultado_envio = envia_email()
    return resultado_envio

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 4000)),host='0.0.0.0',debug=True)