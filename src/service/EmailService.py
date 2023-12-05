from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flask import jsonify
import os, sys, smtplib
from google.cloud import secretmanager
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from model.email import Email

# Implementacao concreta do envio de email
class EmailService:
    load_dotenv()

    def __init__(self):
        self.host = "smtp.mailgun.org" 
        self.port = 587
        

    def envia_email(self, dados_email):
    
        email = Email(
            destinatario = dados_email['destinatario'], 
            assunto = dados_email['assunto'], 
            mensagem = dados_email['mensagem'])

        try: 
            servidor = smtplib.SMTP(self.host, self.port)
            username = self.busca_secrets_keys("MAIL_USERNAME")
            password = self.busca_secrets_keys("MAIL_PASSWORD")
            servidor.starttls()
            servidor.login(username, password)
            mensagem_sistema = MIMEMultipart()
            mensagem_sistema['From'] = 'vaidebike44@gmail.com'
            mensagem_sistema['To'] = email.destinatario
            mensagem_sistema['Subject'] = email.assunto
            body = MIMEText(email.mensagem, 'plain')
            mensagem_sistema.attach(body)
            servidor.send_message(mensagem_sistema)
            servidor.quit()
            return jsonify({"status": "success", "mensagem": "Email enviado com sucesso!"})
        
        except Exception as e:
            return jsonify({"status": "error", "mensagem": f"Erro ao enviar o email: {str(e)}"}), 500
        
    def busca_secrets_keys(self, name_key):
        client = secretmanager.SecretManagerServiceClient()   
        path = f"projects/microservice-externo/secrets/{name_key}/versions/latest"
        response = client.access_secret_version(name=path)
        return response.payload.data.decode("UTF-8")