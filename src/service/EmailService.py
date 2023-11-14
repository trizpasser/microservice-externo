#import smtplib
#from email.mime.text import MIMEText
from unittest.mock import Mock
import re #,os, logging

requests = Mock()

def envia_email(email, assunto, mensagem):
    response_mock = Mock()
    response_mock.status_code = "Email enviado", 200
    response_mock.json.return_value = "Email enviado com sucesso!"
    
    email_existe = True
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' # expressão para validar o formato do email

    if not (re.fullmatch(regex, email)): # confere se está dentro do formato
        response_mock = Mock()
        response_mock.status_code = 422
        response_mock.json.return_value = [
            {
                "codigo": 422,
                "mensagem": "Email com formato inválido."
            }
        ]

        return response_mock.json()

    if not email_existe:
        response_mock = Mock()
        response_mock.status_code = 422
        response_mock.json.return_value = [
            {
                "codigo": 404,
                "mensagem": "Email não existe."
            }
        ]

        return response_mock.json()
    
    

    return response_mock.json()





    '''
    servidor_smtp = "smtp.mail.yahoo.com"
    porta_smtp = 465
    usuario_smtp = "vaidebike3@yahoo.com.br"
    senha_smtp = os.environ.get('SENHA_EMAIL')  # Usar uma variável de ambiente para a senha

    remetente = usuario_smtp
    assunto = "Notificação"
    mensagem = "Você está sendo notificado pelo Vai de Bike!"

    corpo_email = f"Assunto: {assunto}\n\n{mensagem}"

    msg = MIMEText(corpo_email)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    try:
        
        with smtplib.SMTP_SSL(servidor_smtp, porta_smtp) as server:
            server.login(usuario_smtp, senha_smtp)
            server.sendmail(remetente, destinatario, msg.as_string())

        # supostamente envia email

        logging.info(f'E-mail enviado para {destinatario} com sucesso!')
        return 'E-mail enviado com sucesso!'
    except smtplib.SMTPAuthenticationError:
        logging.error("Erro de autenticação SMTP. Verifique as credenciais.")
        return "Erro de autenticação SMTP. Verifique as credenciais."
    except smtplib.SMTPException as e:
        logging.error(f"Erro ao enviar e-mail para {destinatario}: {str(e)}")
        return f"Erro ao enviar e-mail: {str(e)}"
        '''
    
    

