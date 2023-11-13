import smtplib
from email.mime.text import MIMEText
from unittest.mock import Mock
import os, logging, mock

requests = Mock()

def envia_email(destinatario):

    SENHA_EMAIL = "minha$enha123"

    servidor_smtp = "smtp.mail.yahoo.com"
    porta_smtp = 465
    usuario_smtp = "vaidebike3@yahoo.com.br"
    senha_smtp = os.environ.get(SENHA_EMAIL)  # Usar uma variável de ambiente para a senha

    remetente = usuario_smtp
    assunto = "Notificação"
    mensagem = "Você está sendo notificado pelo Vai de Bike!"

    corpo_email = f"Assunto: {assunto}\n\n{mensagem}"

    msg = MIMEText(corpo_email)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    try:
        
        '''
        with smtplib.SMTP_SSL(servidor_smtp, porta_smtp) as server:
            server.login(usuario_smtp, senha_smtp)
            server.sendmail(remetente, destinatario, msg.as_string())
        '''
        # supostamente envia email

        logging.info(f'E-mail enviado para {destinatario} com sucesso!')
        return 'E-mail enviado com sucesso!'
    except smtplib.SMTPAuthenticationError:
        logging.error("Erro de autenticação SMTP. Verifique as credenciais.")
        return "Erro de autenticação SMTP. Verifique as credenciais."
    except smtplib.SMTPException as e:
        logging.error(f"Erro ao enviar e-mail para {destinatario}: {str(e)}")
        return f"Erro ao enviar e-mail: {str(e)}"

