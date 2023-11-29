class Email:
    def __init__(self, destinatario, assunto, mensagem):
        self.destinatario = destinatario
        self.assunto = assunto
        self.mensagem = mensagem

    def __init__(self) -> None: # Noncompliant - method is empty
        pass