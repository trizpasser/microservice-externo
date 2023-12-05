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
        self.username = os.getenv('MAIL_USERNAME')
        self.password = os.getenv('MAIL_PASSWORD')
        

    def envia_email(self, dados_email):
        client = secretmanager.SecretManagerServiceClient()
        project_id = "microservice-externo"
        parent = f"projects/{project_id}"
    
        email = Email(
            destinatario = dados_email['destinatario'], 
            assunto = dados_email['assunto'], 
            mensagem = dados_email['mensagem'])
        try: 
            # Cria uma conexão com o servidor SMTP
            servidor = smtplib.SMTP(self.host, self.port)

            mail_username_path = f"projects/{project_id}/secrets/MAIL_USERNAME/versions/latest"
            response_mail_username = client.acess_secret_version(name=mail_username_path)
            username = response_mail_username.payload.data.decode("UTF-8")

            mail_password_path = f"projects/{project_id}/secrets/MAIL_PASSWORD/versions/latest"
            response_password = client.acess_secret_version(name=mail_password_path)
            password = response_password.payload.data.decode("UTF-8")

            # Autentica-se no servidor
            servidor.starttls()
            servidor.login(username, password)

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
            return jsonify({"status": "error", "var_ambiente": username, "var_password": password, "mensagem": f"Erro ao enviar o email: {str(e)}"})
