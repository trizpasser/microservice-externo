import unittest, os, sys
from unittest.mock import patch

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from controller.main import app

class TestMain(unittest.TestCase):

    @patch('controller.main.Mock')
    def test_cadastrar_bicicletas_route(self, mock_cadastrar_bicicletas):

        mock_cadastrar_bicicletas.status_code = 200

        data = {
            "email": "teste",
            "assunto": "teste",
            "mensagem ": "teste"
        }

        token = "None"
        with app.test_client() as client:
            response = client.get('/get_csrf_token')
            token = response.get_data(as_text=True)
            response = client.post('/enviarEmail', headers={"Content-Type": "application/json", "X-CSRFToken": token}, json=data)
            self.assertEqual(response.status_code, mock_cadastrar_bicicletas.status_code)

    @patch('controller.main.Mock')
    def test_realizar_cobranca_route(self, mock_realiza_cobranca):
        mock_realiza_cobranca.status_code = 200

        data = {
            "valor": 20,
            "ciclista": 1
        }

        token = "None"
        with app.test_client() as client:
            response = client.get('/get_csrf_token')
            token = response.get_data(as_text=True)
            response = client.post('/cobranca', headers={"Content-Type": "application/json", "X-CSRFToken": token}, json=data)
            self.assertEqual(response.status_code, mock_realiza_cobranca.status_code)


    @patch('controller.main.Mock')
    def test_processar_cobrancas_em_fila_route(self, mock_processa_cobrancas_pendentes):
        mock_processa_cobrancas_pendentes.status_code = 200

        token = "None"
        with app.test_client() as client:
            response = client.get('/get_csrf_token')
            token = response.get_data(as_text=True)
            response = client.post('/processaCobrancasEmFila', headers={"Content-Type": "application/json", "X-CSRFToken": token})
            self.assertEqual(response.status_code, mock_processa_cobrancas_pendentes.status_code)

    
    @patch('controller.main.Mock')
    def test_inserir_cobranca_em_fila_route(self, mock_insere_cobranca_na_fila):
        mock_insere_cobranca_na_fila.status_code = 200

        data = {
            "valor": 20.0,
            "ciclista": 2,
        }

        token = "None"
        with app.test_client() as client:
            response = client.get('/get_csrf_token')
            token = response.get_data(as_text=True)
            response = client.post('/filaCobranca', headers={"Content-Type": "application/json", "X-CSRFToken": token}, json=data)
            self.assertEqual(response.status_code, mock_insere_cobranca_na_fila.status_code)


    @patch('controller.main.Mock')
    def test_obter_cobranca_route(self, mock_obtem_cobranca):
        mock_obtem_cobranca.status_code = 200

        with app.test_client() as client:
            response = client.get('/cobranca/1', headers={"Content-Type": "application/json"})
            self.assertEqual(response.status_code, mock_obtem_cobranca.status_code)


    @patch('controller.main.Mock')
    def test_validar_cartao_route(self, mock_valida_cartao):
        mock_valida_cartao.status_code = 200

        data = {
            "cartao": {
                "nome_titular": "Teste Titular",
                "numero": "1234567812345678",
                "validade": "12/24",
                "cvv": "123",
            }
        }
        with app.test_client() as client:
            response = client.get('/get_csrf_token')
            token = response.get_data(as_text=True)
            response = client.post('/validaCartaoDeCredito', headers={"Content-Type": "application/json", "X-CSRFToken": token}, json=data)
            self.assertEqual(response.status_code, mock_valida_cartao.status_code)

if __name__ == '__main__':
    unittest.main()