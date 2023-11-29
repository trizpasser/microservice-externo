from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flask import jsonify
import os
import smtplib
import os, sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from model.email import Email

# Implementacao concreta do envio de email
class EmailService:
    load_dotenv()

    def __init__(self):
        self.host = os.getenv('MAIL_SERVER') 
        self.port = 587
        self.username = os.getenv('MAIL_USERNAME')
        self.password = os.getenv('MAIL_PASSWORD')

    def envia_email(self, dados_email):
        email = Email(
            destinatario = dados_email['destinatario'], 
            assunto = dados_email['assunto'], 
            mensagem = dados_email['mensagem'])

        try: 

            # Cria uma conexão com o servidor SMTP
            servidor = smtplib.SMTP(self.host, self.port)

            # Autentica-se no servidor
            servidor.starttls()
            servidor.login(self.username, self.password)

            # Cria a mensagem de e-mail
            mensagem_sistema = MIMEMultipart()
            mensagem_sistema['From'] = 'vaidebike44@gmail.com'
            mensagem_sistema['To'] = email.destinatario
            mensagem_sistema['Subject'] = email.assunto

            body = MIMEText(email.mensagem, 'plain')
            mensagem_sistema.attach(body)

            # Envia a mensagem de e-mail
            servidor.send_message(mensagem_sistema)

            # Fecha a conexão com o servidor
            servidor.quit()
            
            return jsonify({"status": "success", "mensagem": "Email enviado com sucesso!"})
        
        except Exception as e:
            return jsonify({"status": "error", "mensagem": f"Erro ao enviar o email: {str(e)}"})



