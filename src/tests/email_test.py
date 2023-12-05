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
    def test_envia_email_success(self, mock_smtp):
        # Configurar o retorno desejado para a função busca_secrets_keys
        with patch('service.EmailService.EmailService.busca_secrets_keys', return_value='test_value'):
            email_service = EmailService()

            # Configurar o comportamento do mock_smtp
            mock_smtp_instance = mock_smtp.return_value
            mock_smtp_instance.login.return_value = None

            # Dados de email de teste
            dados_email = {
                'destinatario': 'bqueiroz@edu.unirio.br',
                'assunto': 'Teste',
                'mensagem': 'Olá!'
            }

            # Chamar o método envia_email
            response = email_service.envia_email(dados_email)

            # Verificar se o mock_smtp foi chamado corretamente
            mock_smtp.assert_called_once_with(email_service.host, email_service.port)
            mock_smtp_instance.starttls.assert_called_once()
            mock_smtp_instance.login.assert_called_once_with('vaidebike44@gmail.com', 'test_value')
            mock_smtp_instance.send_message.assert_called_once()

            # Verificar se a resposta está correta
            self.assertEqual(response[0].status_code, 200)
            self.assertEqual(response[1]['status'], 'success')

    @patch('service.EmailService.smtplib.SMTP')
    def test_envia_email_failure(self, mock_smtp):
        # Configurar o retorno desejado para a função busca_secrets_keys
        with patch('service.EmailService.EmailService.busca_secrets_keys', return_value='test_value'):
            email_service = EmailService()

            # Configurar o comportamento do mock_smtp para simular uma exceção
            mock_smtp_instance = mock_smtp.return_value
            mock_smtp_instance.login.side_effect = Exception("Erro ao fazer login")

            # Dados de email de teste
            dados_email = {
                'destinatario': 'bqueiroz@edu.unirio.br',
                'assunto': 'Teste',
                'mensagem': 'Olá!'
            }


            # Chamar o método envia_email
            response = email_service.envia_email(dados_email)

            # Verificar se o mock_smtp foi chamado corretamente
            mock_smtp.assert_called_once_with(email_service.host, email_service.port)
            mock_smtp_instance.starttls.assert_called_once()
            mock_smtp_instance.login.assert_called_once_with('vaidebike44@gmail.com', 'test_value')

            # Verificar se a resposta de erro está correta
            self.assertEqual(response[0].status_code, 500)
            self.assertEqual(response[1]['status'], 'error')


   

if __name__ == '__main__':
    unittest.main()