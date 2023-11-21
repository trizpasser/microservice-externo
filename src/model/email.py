import os, sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

class Email:
    def __init__(self, destinatario, assunto, mensagem):
        self.destinatario = destinatario
        self.assunto = assunto
        self.mensagem = mensagem

    def __init__(self) -> None: # Noncompliant - method is empty
        pass