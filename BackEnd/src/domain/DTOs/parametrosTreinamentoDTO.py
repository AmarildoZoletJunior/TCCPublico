# DTO para ParametrosTreinamento
class ParametrosTreinamentoDTO:
    def __init__(self, APId, APNumPca, APQtdeRecomendacoes, APIdArquivoProduto, APIdUsuario, arquivo_produto=None, usuario=None):
        self.APId = APId
        self.APNumPca = APNumPca
        self.APQtdeRecomendacoes = APQtdeRecomendacoes
        self.APIdArquivoProduto = APIdArquivoProduto
        self.APIdUsuario = APIdUsuario
        self.arquivo_produto = arquivo_produto
        self.usuario = usuario
        
        
        
    def to_dict(self):
        return {
            "APId": self.APId,
            "APNumPca": self.APNumPca,
            "APQtdeRecomendacoes": self.APQtdeRecomendacoes,
            "APIdArquivoProduto": self.APIdArquivoProduto,
            "APIdUsuario": self.APIdUsuario,
            "arquivo_produto": self.arquivo_produto.to_dict() if self.arquivo_produto else None,
            "usuario": self.usuario.to_dict() if self.usuario else None,
        }