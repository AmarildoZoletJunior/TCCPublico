# DTO para ParametrosTreinamento
class ParametrosTreinamentoDTO:
    def __init__(self, APId, APNumPca, APQtdeRecomendacoes, APIdArquivoProduto, APIdUsuario):
        self.APId = APId
        self.APNumPca = APNumPca
        self.APQtdeRecomendacoes = APQtdeRecomendacoes
        self.APIdArquivoProduto = APIdArquivoProduto
        self.APIdUsuario = APIdUsuario
        
        
        
    def to_dict(self):
        return {
            "APId": self.APId,
            "APNumPca": self.APNumPca,
            "APQtdeRecomendacoes": self.APQtdeRecomendacoes,
            "APIdArquivoProduto": self.APIdArquivoProduto,
            "APIdUsuario": self.APIdUsuario,
        }