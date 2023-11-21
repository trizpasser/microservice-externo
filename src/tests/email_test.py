import unittest, os, sys
from unittest.mock import patch

from flask import Flask

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from service.EmailService import EmailService


class TestEmailService(unittest.TestCase):
     
    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

   
    @patch('service.EmailService.smtplib.SMTP')
    def test_envia_email_sucesso(self, mock_smtp):
        # Configuração do mock
        mock_instance = mock_smtp.return_value

        # Configuração do método de autenticação
        mock_instance.starttls.return_value = True
        mock_instance.login.return_value = True

        # Execução do teste
        destinatario = 'destinatario@example.com'
        assunto = 'Assunto do E-mail'
        mensagem = 'Corpo do E-mail'

        objeto_email = EmailService()
        resultado = objeto_email.envia_email(destinatario, assunto, mensagem)

        # Verificações
        mock_instance.starttls.assert_called_once()
        mock_instance.login.assert_called_once_with(objeto_email.username, objeto_email.password)
        mock_instance.send_message.assert_called_once()

        self.assertEqual(resultado.status_code, 200)
        self.assertEqual(resultado.json, {"status": "success", "mensagem": "Email enviado com sucesso!"})

   

if __name__ == '__main__':
    unittest.main()