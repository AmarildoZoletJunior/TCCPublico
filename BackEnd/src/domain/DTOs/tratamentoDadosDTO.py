# DTO para TratamentoDados
class TratamentoDadosDTO:
    def __init__(self, TDId, TDConfiguracoesAdicionais, TDValorFiltro, TDOperacao, TDIdArquivoProduto, TDIdUsuario, arquivo_produto=None, usuario=None):
        self.TDId = TDId
        self.TDConfiguracoesAdicionais = TDConfiguracoesAdicionais
        self.TDValorFiltro = TDValorFiltro
        self.TDOperacao = TDOperacao
        self.TDIdArquivoProduto = TDIdArquivoProduto
        self.TDIdUsuario = TDIdUsuario
        self.arquivo_produto = arquivo_produto
        self.usuario = usuario
        
        
    def to_dict(self):
        return {
            "TDId": self.TDId,
            "TDConfiguracoesAdicionais": self.TDConfiguracoesAdicionais,
            "TDValorFiltro": self.TDValorFiltro,
            "TDOperacao": self.TDOperacao,
            "TDIdArquivoProduto": self.TDIdArquivoProduto,
            "TDIdUsuario": self.TDIdUsuario,
            "arquivo_produto": self.arquivo_produto.to_dict() if self.arquivo_produto else None,
            "usuario": self.usuario.to_dict() if self.usuario else None,
        }