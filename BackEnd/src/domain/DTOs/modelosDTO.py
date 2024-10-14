# DTO para Modelos
class ModelosDTO:
    def __init__(self, MDId, MDVersao, MDArquivo, MDIdArquivoProd, MDIdUsuario, MDDataPostagem, usuario=None, arquivo_produto=None):
        self.MDId = MDId
        self.MDVersao = MDVersao
        self.MDArquivo = MDArquivo
        self.MDIdArquivoProd = MDIdArquivoProd
        self.MDIdUsuario = MDIdUsuario
        self.MDDataPostagem = MDDataPostagem
        self.usuario = usuario
        self.arquivo_produto = arquivo_produto
        
    def to_dict(self):
        return {
            "MDId": self.MDId,
            "MDVersao": self.MDVersao,
            "MDArquivo": self.MDArquivo,
            "MDIdArquivoProd": self.MDIdArquivoProd,
            "MDIdUsuario": self.MDIdUsuario,
            "MDDataPostagem": self.MDDataPostagem,
            "usuario": self.usuario.to_dict() if self.usuario else None,
            "arquivo_produto": self.arquivo_produto.to_dict() if self.arquivo_produto else None,
        }