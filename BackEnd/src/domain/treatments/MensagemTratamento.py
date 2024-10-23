class MensagemTratamentos():
    def __init__(self,linhaComando,QtdeRegistrosAlterados,tipoOperacao):
            self.linhaComando = linhaComando
            self.QtdeRegistrosAlterados = QtdeRegistrosAlterados
            self.operacao = tipoOperacao
            

    def MontarJson(self):
        MensagemJson = {"TratamentoAvisos":{
            "LinhaComandoTratamento": self.linhaComando,
            "QtdeRegistrosAlterados":self.QtdeRegistrosAlterados,
            "TipoOperacao":self.operacao
        }}
        return MensagemJson