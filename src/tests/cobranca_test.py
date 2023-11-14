import unittest, os, sys
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from service.CobrancaService import realiza_cobranca, processa_cobrancas_pendentes, insere_cobranca_na_fila, obtem_cobranca, valida_cartao

class TestCobrancaService(unittest.TestCase):

    @patch('service.CobrancaService.Mock')
    def test_realiza_cobranca(self, mock_request):
        valor, ciclista = 20.0, "123"
        response_mock = Mock()
        response_mock.status_code = 200

        response_mock.json.return_value = {
            "id": 1,
            "status": "Pago",
            "horaSolicitacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "horaFinalizacao": (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
            "valor": valor,
            "ciclista": ciclista
        }

        mock_request.return_value = response_mock
        result = realiza_cobranca(valor, ciclista)
        
        self.assertEqual(result['status'], "Pago")
        self.assertEqual(result['valor'], valor)
        self.assertEqual(result['ciclista'], ciclista)

   
    @patch('service.CobrancaService.Mock')
    @patch('service.CobrancaService.Fila')
    def test_processa_cobrancas_pendentes(self, mock_fila, mock_request):
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = "Todas as cobrancas foram quitadas!"

        # Configurando mock_fila para retornar False quando confere_se_vazia for chamado
        mock_fila.return_value.confere_se_vazia.return_value = False

        # Configurando mock_fila para retornar uma cobrança quando obtem_cobranca for chamado
        mock_fila.return_value.obtem_cobranca.return_value = {
            "id": 1,
            "status": "Pendente",
            "valor": 20.0,
            "ciclista": "123"
        }

        result = processa_cobrancas_pendentes()
        self.assertEqual(result, "Todas as cobrancas foram quitadas!")

    @patch('service.CobrancaService.Mock')
    def test_insere_cobranca_na_fila(self, mock_request):
        valor, ciclista = 20.0, "123"
        response_mock = Mock()
        response_mock.status_code = 200

        response_mock.json.return_value = {
            "id": 1,
            "status": "Pendente",
            "horaSolicitacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "horaFinalizacao": "-",
            "valor": valor,
            "ciclista": ciclista
        }

        mock_request.return_value = response_mock
        result = insere_cobranca_na_fila(valor, ciclista)

        self.assertEqual(result['status'], "Pendente")
        self.assertEqual(result['valor'], valor)
        self.assertEqual(result['ciclista'], ciclista)

    @patch('service.CobrancaService.Mock')
    def test_obtem_cobranca(self, mock_request):
        id_cobranca = 1
        response_mock = Mock()
        response_mock.status_code = 200

        response_mock.json.return_value = {
            "id": id_cobranca,
            "status": "Pago",
            "horaSolicitacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "horaFinalizacao": (datetime.now() + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"),
            "valor": 20.0,
            "ciclista": "123"
        }

        mock_request.return_value = response_mock
        result = obtem_cobranca(id_cobranca)

        self.assertEqual(result['id'], id_cobranca)
        self.assertEqual(result['status'], "Pago")
        self.assertEqual(result['valor'], 20.0)
        self.assertEqual(result['ciclista'], "123")

    @patch('service.CobrancaService.Mock')
    def test_valida_cartao(self, mock_request):
        nome_titular, numero, validade, cvv = "João da Silva", "1234567890123456", "12/24", "123"
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = "Dados atualizados!"

        mock_request.return_value = response_mock
        result = valida_cartao(nome_titular, numero, validade, cvv)

        self.assertEqual(result, "Dados atualizados!")

if __name__ == '__main__':
    unittest.main()