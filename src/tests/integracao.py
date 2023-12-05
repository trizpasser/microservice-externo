import unittest, os, sys
from unittest.mock import patch


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from service.CobrancaService import CobrancaService

@patch('service.CobrancaService.requests.get')
class TestRoutes(unittest.TestCase):
    def test_obtem_dados_cartao_sucesso(self, mock_get):
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {"campo1": "valor1", "campo2": "valor2"}

        seu_servico = CobrancaService()

        resultado = seu_servico.obtem_dados_cartao("ciclista123")
        print(resultado)

        self.assertEqual(resultado, {"campo1": "valor1", "campo2": "valor2"})


if __name__ == '__main__':
    unittest.main()