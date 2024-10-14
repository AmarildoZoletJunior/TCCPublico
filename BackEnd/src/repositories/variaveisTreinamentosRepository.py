from data.database import Database
from domain.entities.variaveisTreinamentos import VariaveisTreinamentos


class VariaveisTreinamentoRepository():
    def __init__(self,data):
        self.Data = data
        
        self.mapa_tipos = {
            1: str,
            2: int,
            3: bool,
            4: float
        }
    
    def FindVariableById(self,idVariable):
        data = Database()
        response = data.DoSelect(VariaveisTreinamentos,VTId=idVariable)
        if len(response) == 0:
            return 400,'Variável não encontrada.',()
        return 200,'',response