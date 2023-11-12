from flask import request
from email.mime.text import MIMEText
import smtplib 
import logging

def envia_email(destinatario):

    #destinatario = request.form.get('destinatario')
    #assunto = request.form.get('assunto')
    #mensagem = request.form.get('mensagem')

    servidor_smtp = "smtp.gmail.com"
    porta_smtp = 587
    usuario_smtp = "vaidebike44@gmail.com"
    senha_smtp = "minha$enha123"  #modificar para alternativa segura
    
    remetente = usuario_smtp
    assunto = "Notificação"
    mensagem = "Você está sendo notificado pelo Vá de Bike!"

    corpo_email = f"Assunto: {assunto}\n\n{mensagem}"

    msg = MIMEText(corpo_email)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario

    try:
        server = smtplib.SMTP(servidor_smtp, porta_smtp)
        server.starttls()
        server.login(usuario_smtp, senha_smtp)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()

        logging.info(f'E-mail enviado para {destinatario} com sucesso!')
        return 'E-mail enviado com sucesso!'
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail para {destinatario}: {str(e)}")
        return f"Erro ao enviar e-mail: {str(e)}"

    #    return 'E-mail enviado.'
    #except Exception as e:
    #    return f"Erro ao enviar e-mail: {str(e)}"