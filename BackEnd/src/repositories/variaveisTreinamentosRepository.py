from src.domain.enum.tipoDado import TipoDado
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
        
        self.mapa_tipos_str = {
            1: 'str',
            2: 'int',
            3: 'bool',
            4: 'float'
        }
    
    def FindVariableById(self,idVariable):
        data = Database()
        response = data.DoSelect(VariaveisTreinamentos,VTId=idVariable)
        if len(response) == 0:
            return 400,'Variável não encontrada.',()
        return 200,'',response
    
    def CreateVariable(self):
        tipoDado = self.Data.get('tipoDado')
        nomeVariavel =  self.Data.get('nomeVariavel')
        tipoDadoConvertido = self.mapa_tipos_str.get(tipoDado)
        response,message = self.ValidVariable(nomeVariavel,tipoDado)
        if response == 400:
            return response,message
        
        if tipoDado not in self.mapa_tipos:
            return 400, "Tipo digitado em tipoDado é inválido."
        
        data = Database()
        response = data.DoSelect(VariaveisTreinamentos,VTNome=nomeVariavel)
        if len(response) > 0:
            return 400,'Não é possível adicionar esta variável pois já existe outra com o mesmo nome.'
        
        response = data.DoInsert(VariaveisTreinamentos,VTNome=nomeVariavel,VTTipoDado = tipoDadoConvertido)
        if response is None:
            return 400,'Não foi possível inserir o registro, tente novamente.'
        return 200,''
        
    def DeleteVariable(self,idVariable):
        data = Database()
        response = data.DoSelect(VariaveisTreinamentos,VTId=idVariable)
        if len(response) == 0:
            return 400,'Variável não encontrada.'
        response = data.DoDelete(VariaveisTreinamentos,VTId = idVariable)
        if response is None:
            return 400,'Não foi possível deletar o registro, tente novamente.'
        return 200,''
    
    def UpdateVariable(self,idVariable):
        tipoDado = self.Data.get('tipoDado')
        nomeVariavel =  self.Data.get('nomeVariavel')
        tipoDadoConvertido = self.mapa_tipos_str.get(tipoDado)
        data = Database()
        response = data.DoSelect(VariaveisTreinamentos,VTId=idVariable)
        if len(response) == 0:
            return 400,'Variável não encontrada.'
        response,message = self.ValidVariable(nomeVariavel,tipoDado)
        if response == 400:
            return response,message
        
        if tipoDado not in self.mapa_tipos:
            return 400, "Tipo digitado em tipoDado é inválido."
        
        response = data.DoUpdate(VariaveisTreinamentos,{"VTId":idVariable},{"VTNome":nomeVariavel,"VTTipoDado":tipoDadoConvertido})
        if response is None:
            return 400,'Não foi possível editar o registro, tente novamente.'
        return 200,''
    
    def ValidVariable(self,nomeVariavel,tipoDado):
        if nomeVariavel is None:
            return 400, 'A propriedade nomeVariavel é obrigatória.'
        
        if not isinstance(nomeVariavel,str):
            return 400,'A propriedade nomeVariavel só aceita tipo de dado texto.'
        if len(nomeVariavel) < 2:
            return 400,'O nome atribuído a variável não pode ter menos de 2 letras.'
        
        if tipoDado is None:
            return 400, 'A propriedade tipoDado é obrigatória.'
        if not isinstance(tipoDado,int):
            return 400,'A propriedade tipoDado do só aceita tipo de dado inteiro.'
        
        return 200,''
    
    def SelectAllVariable(self,):
        data = Database()
        response = data.DoSelect(VariaveisTreinamentos)
        return response