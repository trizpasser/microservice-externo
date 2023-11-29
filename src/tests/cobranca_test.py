import unittest, os, sys
from unittest.mock import patch, Mock
from datetime import datetime, timedelta

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from service.CobrancaService import Cobranca, Fila


class TestCobrancaService(unittest.TestCase):

    def setUp(self):
        self.cobranca = Cobranca()

   
    def test_lista_cobrancas(self): # remover 
        resultado = self.cobranca.lista_cobrancas()
        self.assertIsInstance(resultado, list)
        self.assertGreater(len(resultado), 0)
        self.assertIsInstance(resultado[0], dict)
        self.assertIn("id", resultado[0])
        self.assertIn("ciclista", resultado[0])
        self.assertIn("status", resultado[0])
        self.assertIn("horaSolicitacao", resultado[0])
        self.assertIn("horaFinalizacao", resultado[0])
        self.assertIn("valor", resultado[0])

    def test_realiza_cobranca(self):
        valor = 50
        ciclista = "Joao"
        resultado, status_code = self.cobranca.realiza_cobranca(valor, ciclista)

        self.assertEqual(status_code, 200)
        self.assertIsInstance(resultado, dict)
        self.assertIn("id", resultado)
        self.assertIn("status", resultado)
        self.assertIn("horaSolicitacao", resultado)
        self.assertIn("horaFinalizacao", resultado)
        self.assertIn("valor", resultado)
        self.assertIn("ciclista", resultado)

    def test_processa_cobrancas_pendentes(self):
    
        resultado, status_code = self.cobranca.processa_cobrancas_pendentes()
        self.assertEqual(status_code, 200)
        self.assertEqual(resultado, "Todas as cobrancas foram quitadas!")

    def test_insere_cobranca_na_fila(self):
        valor = 30
        ciclista = "Maria"
        resultado, status_code = self.cobranca.insere_cobranca_na_fila(valor, ciclista)

        self.assertEqual(status_code, 200)
        self.assertIsInstance(resultado, list)
        self.assertGreater(len(resultado), 0)
        self.assertIsInstance(resultado[0], dict)
        self.assertIn("id", resultado[0])
        self.assertIn("status", resultado[0])
        self.assertIn("horaSolicitacao", resultado[0])
        self.assertIn("horaFinalizacao", resultado[0])
        self.assertIn("valor", resultado[0])
        self.assertIn("ciclista", resultado[0])

    def test_obtem_cobranca_existente(self):
        id_cobranca_existente = 1
        resultado, status_code = self.cobranca.obtem_cobranca(id_cobranca_existente)

        self.assertEqual(status_code, 200)
        self.assertIsInstance(resultado, dict)
        self.assertIn("id", resultado)
        self.assertIn("ciclista", resultado)
        self.assertIn("status", resultado)
        self.assertIn("horaSolicitacao", resultado)
        self.assertIn("horaFinalizacao", resultado)
        self.assertIn("valor", resultado)

    def test_obtem_cobranca_inexistente(self):
        id_cobranca_inexistente = 999
        resultado, status_code = self.cobranca.obtem_cobranca(id_cobranca_inexistente)

        self.assertEqual(status_code, 400)
        self.assertEqual(resultado, "Dados não encontrados")

    def test_valida_cartao_valido(self):
        nome_titular = "Joao Silva"
        numero = "1234567890123456"
        validade = "12/25"
        cvv = "123"

        resultado, status_code = self.cobranca.valida_cartao(nome_titular, numero, validade, cvv)

        self.assertEqual(status_code, 200)
        self.assertEqual(resultado, "Cartão válido!")

    def test_valida_cartao_invalido(self):
       
        nome_titular = ""
        numero = "1234"
        validade = "01/21"
        cvv = ""

        resultado, status_code = self.cobranca.valida_cartao(nome_titular, numero, validade, cvv)

        self.assertEqual(status_code, 400)
        self.assertEqual(resultado, "Cartão inválido")

if __name__ == '__main__':
    unittest.main()