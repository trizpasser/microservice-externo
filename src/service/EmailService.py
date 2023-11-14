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

    if email_existe:
       
       return response_mock.json()

    else: 
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