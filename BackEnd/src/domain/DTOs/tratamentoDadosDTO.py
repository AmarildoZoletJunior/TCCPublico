# DTO para TratamentoDados
class TratamentoDadosDTO:
    def __init__(self, TDId, TDConfiguracoesAdicionais, TDValorFiltro, TDOperacao, TDIdArquivoProduto, TDIdUsuario):
        self.TDId = TDId
        self.TDConfiguracoesAdicionais = TDConfiguracoesAdicionais
        self.TDValorFiltro = TDValorFiltro
        self.TDOperacao = TDOperacao
        self.TDIdArquivoProduto = TDIdArquivoProduto
        self.TDIdUsuario = TDIdUsuario
        
        
    def to_dict(self):
        return {
            "TDId": self.TDId,
            "TDConfiguracoesAdicionais": self.TDConfiguracoesAdicionais,
            "TDValorFiltro": self.TDValorFiltro,
            "TDOperacao": self.TDOperacao,
            "TDIdArquivoProduto": self.TDIdArquivoProduto,
            "TDIdUsuario": self.TDIdUsuario
        }