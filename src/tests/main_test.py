import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from flask import Flask
import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from controller.main import app, email, cobranca  

class TestController(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()



    @patch('controller.main.enviar_email_route')
    def test_enviar_email_route_500(self, mock_enviar_email):
       email_json = {"destinatario": "", "assunto": "teste unitario", "mensagem": "corpo do teste de email"}
      

       response = self.client.post('/enviarEmail', headers={"Content-Type": "application/json"}, json= {"destinatario": "bqueiroz@edu.unirio.br", "assunto": "teste unitario", "mensagem": "corpo do teste de email"} )

       self.assertEqual(response.status_code, 500)
       

    @patch('controller.main.realizar_cobranca_route')
    def test_realizar_cobranca_route_200(self, mock_realiza_cobranca):
        mock_realiza_cobranca.return_value = {
            "-Status-": "Cobrança realizada com sucesso!", 
            "status:": "Paga",
            "valor": 100,
            "ciclista": "100"
            }

        data = {"valor": 100, "ciclista": "100"}

        response = self.client.post('/cobranca', headers={"Content-Type": "application/json"}, json=data)

        self.assertEqual(response.status_code, 200)
        

    @patch('controller.main.processar_cobrancas_em_fila_route')
    def test_realizar_cobranca_route_200(self, mock):
        mock.return_value = "Todas as cobrancas foram quitadas!", 200
        data = {"valor": 100, "ciclista": "100"}
        response = self.client.post('/processaCobrancasEmFila', headers={"Content-Type": "application/json"}, json=data)
        self.assertEqual(response.status_code, 200)

    @patch('controller.main.obter_cobranca_route')
    def teste_obter_cobranca_route_200(self, mock_obter_cobranca):
        mock_obter_cobranca.return_value = {
        
            "id": 1,
            "ciclista": "123",
            "status": "Pago",
            "horaSolicitacao": "2023-11-13 02:14:39",
            "horaFinalizacao": "2023-11-13 02:19:39",
            "valor": 10.0
        }
        response = self.client.get('/cobranca/1')

        self.assertEqual(response.status_code, 200)

    @patch('controller.main.inserir_cobranca_em_fila_route')
    def teste_inserir_cobranca_em_fila_route_200(self, mock_inserir_cobranca_em_fila):
        mock_inserir_cobranca_em_fila.return_value = "Cobranca registrada como pendente", 200
        data = {"valor": 10, "ciclista": "123"}
        response = self.client.post('/filaCobranca', headers={"Content-Type": "application/json"}, json=data)

        self.assertEqual(response.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()
