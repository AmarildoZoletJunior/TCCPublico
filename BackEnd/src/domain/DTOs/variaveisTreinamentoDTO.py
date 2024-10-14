# DTO para VariaveisTreinamentos
class VariaveisTreinamentosDTO:
    def __init__(self, VTId, VTNome, VTTipoDado):
        self.VTId = VTId
        self.VTNome = VTNome
        self.VTTipoDado = VTTipoDado
        
    
    def to_dict(self):
        return {
            "VTId": self.VTId,
            "VTNome": self.VTNome,
            "VTTipoDado": self.VTTipoDado,
        }