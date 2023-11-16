from dotenv import load_dotenv
import os



def envia_email(email, assunto, mensagem):
    load_dotenv()
   
    senha = os.getenv('EMAIL_PASSWORD')
    remetente = os.getenv('EMAIL_SENDER')

    ''' # mensagens de erro pertencem ao front
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b' # expressão para validar o formato do email

    if not (re.fullmatch(regex, email)): # confere se está dentro do formato
        response_mock = Mock()
        response_mock.status_code = 422
        response_mock.json.return_value = {
            "codigo": 422,
            "mensagem": "Email com formato inválido."
        }

        return response_mock.json()

    '''
    
    return 1
    