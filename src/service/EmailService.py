from unittest.mock import Mock
import re #,os, logging

requests = Mock()

def envia_email(email, assunto, mensagem):
    response_mock = Mock()
    response_mock.status_code = "Email enviado", 200
   
    response_mock.json.return_value = [
        {
            "msg": "Email enviado com sucesso!",
            "email": email,
            "assunto": assunto,
            "mensagem": mensagem,
        }
    ]

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
    
    return response_mock.json()
    