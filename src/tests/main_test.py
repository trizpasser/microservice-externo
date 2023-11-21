import unittest
from unittest.mock import MagicMock
from flask import Flask
import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from controller.main import app, email, cobranca  # Substitua "seu_modulo" pelo nome real do seu módulo

class TestController(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_hello_world(self):
        response = self.app.get('/')
        self.assertEqual(response.data.decode('utf-8'), "Hello World! :)")

    def test_enviar_email_route(self):
        email.envia_email = MagicMock(return_value={"status": "success", "mensagem": "Email enviado com sucesso!"})
        response = self.app.post('/enviarEmail', json={"destinatario": "test@example.com", "assunto": "Teste", "mensagem": "Corpo do e-mail"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "success", "mensagem": "Email enviado com sucesso!"})
        email.envia_email.assert_called_once_with("test@example.com", "Teste", "Corpo do e-mail")

    def test_realizar_cobranca_route(self):
        cobranca.realiza_cobranca = MagicMock(return_value=({"id": 1, "status": "Pago", "valor": 20.0, "ciclista": 123}, 200))
        response = self.app.post('/cobranca', json={"valor": 20.0, "ciclista": 123})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"id": 1, "status": "Pago", "valor": 20.0, "ciclista": 123})
        cobranca.realiza_cobranca.assert_called_once_with(20.0, 123)

    # Adicione mais testes para os outros métodos

if __name__ == '__main__':
    unittest.main()
