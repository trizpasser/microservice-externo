import unittest
from unittest.mock import MagicMock
from flask import Flask
import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from controller.main import app, email, cobranca  

class TestController(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_hello_world(self):
        response = self.app.get('/')
        self.assertEqual(response.data.decode('utf-8'), "Hello World! :)")

    @patch('controller.main.enviar_email_route')
    def test_enviar_email_route_200(self, mock_enviar_email):
       email_json = {"destinatario": "bqueiroz@edu.unirio.br", "assunto": "teste unitario", "mensagem": "corpo do teste de email"}
       mock_enviar_email.return_value = {
        "mensagem": "Email enviado com sucesso!",
        "status": "success"}
       response = self.client.post('/enviarEmail', headers={"Content-Type": "application/json"}, json=email_json )

       self.assertEqual(response.status_code, 200)
       self.assertEqual(response.return_value, mock_enviar_email.return_value)
    



    @patch('controller.main.enviar_email_route')
    def test_enviar_email_route_500(self, mock_enviar_email):
       email_json = {"destinatario": "", "assunto": "teste unitario", "mensagem": "corpo do teste de email"}
      

       response = self.client.post('/enviarEmail', headers={"Content-Type": "application/json"}, json=email_json )

       self.assertEqual(response.status_code, 500)
       

    @patch('controller.main.cobranca.realizar_cobranca_route')
    def test_realizar_cobranca_route_200(self, mock_realiza_cobranca):
        mock_realiza_cobranca.return_value = {
            "-Status-": "Cobrança realizada com sucesso!", 
            "status:": "Paga"
            "valor": 100
            "ciclista": "100"
            }

        data = {"valor": 100, "ciclista": "100"}

        response = self.client.post('/cobranca', headers={"Content-Type": "application/json"}, json=data)

        self.assertEqual(response.status_code, 200)
        

    @patch('controller.main.cobranca.processar_cobrancas_em_fila_route')
    def test_realizar_cobranca_route_200(self, mock):
        mock.return_value = "Todas as cobrancas foram quitadas!", 200
        data = {"valor": 100, "ciclista": "100"}
        response = self.client.post('/processaCobrancaEmFila', headers={"Content-Type": "application/json"}, json=data)
        self.assertEqual(response.status_code, 200)

    
    @patch('controller.main.cobranca.inserir_cobranca_em_fila_route')
    def test_realizar_cobranca_route_422(self, mock):
        mock.return_value = {
             "codigo": 422,
             "mensagem": "Dados inválidos"
            }, 422

        data = {"valor": "ad" , "ciclista": ""}
        
        response = self.client.post('/filaCobranca', headers={"Content-Type": "application/json"}, json=data)
        self.assertEqual(response.return_value, mock.return_value)


if __name__ == '__main__':
    unittest.main()
