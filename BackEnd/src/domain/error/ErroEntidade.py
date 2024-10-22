class ErroEntidade():
    def __init__(self):
        self.ListaErros = []
    
    def AdicionarMensagem(self,NomeAtributo,Mensagem):
        MensagemJson = {
            "Mensagem":Mensagem,
            "Atributo":NomeAtributo
        }
        self.ListaErros.append(MensagemJson)
        return self.ListaErros