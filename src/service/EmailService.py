from dotenv import load_dotenv
import os, requests

class Email:

    def teste(email):
        load_dotenv()
    
        API_KEY = os.getenv('API_KEY')

        return requests.post(
            "https://api.mailgun.net/v3/YOUR_DOMAIN_NAME/messages",
            auth=("api", API_KEY),
            data={"from": "Excited User <mailgun@sandbox4ae25e8eead44616a86246087ced0de3.mailgun.org>",
                "to": [email, "grupoC@sandbox4ae25e8eead44616a86246087ced0de3.mailgun.org"],
                "subject": "Hello",
                "text": "Testing some Mailgun awesomeness!"})

    def envia_email(email, assunto, mensagem):
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
        