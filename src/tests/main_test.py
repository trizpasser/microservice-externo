import unittest, os, sys
from unittest.mock import patch

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from controller.main import app

class TestMain(unittest.TestCase):

    @patch('controller.main.Mock')
    def test_enviar_email_route(self, mock_enviar_email):

        mock_enviar_email.status_code = 200

        data = {
            "email": "teste@email.com",
            "assunto": "teste",
            "mensagem": "teste",
        }
        token = "None"
        with app.test_client() as client:
            response = client.get('/get_csrf_token')
            token = response.get_data(as_text=True)
            response = client.post('/bicicleta', headers={"Content-Type": "application/json", "X-CSRFToken": token}, json=data)
            self.assertEqual(response.status_code, mock_enviar_email.status_code)