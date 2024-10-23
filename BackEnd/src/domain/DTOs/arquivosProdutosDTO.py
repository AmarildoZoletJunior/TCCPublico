# DTO para ArquivoProdutos
class ArquivoProdutosDTO:
    def __init__(self, APId, APQtdeProdutos, APDataPostagem, APArquivo, APIdUsuario, APVersao,APArquivoDelimiter, usuario=None, modelos=None, parametros_treinamentos=None, tratamentos_dados=None):
        self.APId = APId
        self.APQtdeProdutos = APQtdeProdutos
        self.APDataPostagem = APDataPostagem
        self.APArquivo = APArquivo
        self.APIdUsuario = APIdUsuario
        self.APVersao = APVersao
        self.APArquivoDelimiter = APArquivoDelimiter
        self.usuario = usuario
        self.modelos = modelos
        self.parametros_treinamentos = parametros_treinamentos
        self.tratamentos_dados = tratamentos_dados


    def to_dict(self):
        return {
            "APId": self.APId,
            "APQtdeProdutos": self.APQtdeProdutos,
            "APDataPostagem": self.APDataPostagem,
            "APArquivo": self.APArquivo,
            "APIdUsuario": self.APIdUsuario,
            "APVersao": self.APVersao,
            "APArquivoDelimiter": self.APArquivoDelimiter,
            "modelos": [modelo.to_dict() for modelo in self.modelos] if self.modelos else None,
            "parametros_treinamentos": [parametro.to_dict() for parametro in self.parametros_treinamentos] if self.parametros_treinamentos else None,
            "tratamentos_dados": [tratamento.to_dict() for tratamento in self.tratamentos_dados] if self.tratamentos_dados else None,
        }