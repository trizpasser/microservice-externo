import unittest, os, sys
from unittest.mock import patch, Mock

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from service.EmailService import envia_email

class TestEmailService(unittest.TestCase):
     @patch('service.EmailService.Mock')
     def test_envia_email(self, mock_request):
        email, assunto, mensagem = "teste@email.com", "TesteAssunto", "Ola Mundo"
        response_mock = Mock()
        response_mock.status_code = 200
    
        response_mock.json.return_value = {
            "email": email,
            "assunto": assunto,
            "mensagem": mensagem

        }
        mock_request.return_value = response_mock
        result = envia_email(email, assunto, mensagem)
        self.assertEqual(result['email'], email)  
        self.assertEqual(result['mensagem'], mensagem)

if __name__ == '__main__':
    unittest.main()