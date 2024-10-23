class ErroEntidade():
    def __init__(self,MensagemErro,AtributoNome,LinhaComando):
        MensagemJson = {"ErroTratamento":{
            "MensagemErro": MensagemErro,
            "Atributo":AtributoNome,
            "LinhaComando":LinhaComando
        }}
        return MensagemJson
    