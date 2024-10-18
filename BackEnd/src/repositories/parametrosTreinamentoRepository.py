from domain.entities.arquivosProdutos import ArquivoProdutos
from domain.entities.parametrosTreinamentos import ParametrosTreinamento
from domain.entities.usuarios import Usuarios
from data.database import Database


class ParametrosTreinamentoRepository():
    def __init__(self,data):
        self.Data=data
        
    def CreateParametersToData(self):
        numPca = self.Data.get('numPca')
        qtdeRecomendacao = self.Data.get('qtdeRecomendacao')
        usuId = self.Data.get('usuId')
        ArquivoId = self.Data.get('arquivoId')
        
        response,message  = self.ValidParameters(numPca,qtdeRecomendacao,usuId,ArquivoId)
        if not response:
            return 400,message
        
        Data = Database()
        fileExist = Data.DoSelect(ArquivoProdutos,APId=ArquivoId)
        if len(fileExist) == 0:
            return 400,'Não foi encontrado o dataset de produto neste ID.'
        
        
        
        if numPca > fileExist[0]['APQtdeProdutos']:
            return 400,'Não é possível gerar este número de componente pois a quantidade é superior ao total de produtos que existem neste DataSet.'
        
        if qtdeRecomendacao > fileExist[0]['APQtdeProdutos']:
            return 400,'Não é possível gerar este número de recomendações pois a quantidade é superior ao total de produtos que existem neste DataSet.'
        
        
        
        userExist = Data.DoSelect(Usuarios,USUid=usuId)
        if len(userExist) == 0:
            return 400,'O usuário não existe.'
        
        registerExist = Data.DoSelect(ParametrosTreinamento,APNumPca = numPca,APQtdeRecomendacoes = qtdeRecomendacao ,APIdArquivoProduto = ArquivoId)
        if len(registerExist) > 0:
            return 400,'Já existe um registro com estes parâmetros de treinamento para este dataset.'
        
        response = Data.DoInsert(ParametrosTreinamento,APNumPca=numPca,APQtdeRecomendacoes=qtdeRecomendacao,APIdArquivoProduto=ArquivoId,APIdUsuario=usuId)
        if response is None:
            return 400,'Não foi possível inserir o registro. Tente novamente.'
        
        return 200,''
        
    def ModifyParametersData(self,idParametro):
        numPca = self.Data.get('numPca')
        qtdeRecomendacao = self.Data.get('qtdeRecomendacao')
        ArquivoId = self.Data.get('arquivoId')
        usuId = self.Data.get('usuId')
        
        
        response,message = self.ValidParameters(numPca,qtdeRecomendacao,usuId,ArquivoId)
        if not response:
            return 400,message
        Data = Database()
        registerExist = Data.DoSelect(ParametrosTreinamento,APId=idParametro)
        if len(registerExist) == 0:
            return 400,'Parametros não encontrado.'
        fileExist = Data.DoSelect(ArquivoProdutos,APId=ArquivoId)
        if len(fileExist) == 0:
            return 400,'Não foi encontrado o dataset de produto neste ID.'
        
        userExist = Data.DoSelect(Usuarios,USUid=usuId)
        if len(userExist) == 0:
            return 400,'O usuário não existe.'
        
        
        
        response = Data.DoUpdate(ParametrosTreinamento,{"APId":idParametro},{"APQtdeRecomendacoes":qtdeRecomendacao,"APNumPca":numPca,"APIdUsuario":usuId,"APIdArquivoProduto":ArquivoId})
        if response is None:
            return 400,'Ocorreu um erro ao modificar o registro. Tente novamente.'
        return 200,''
        
    def ValidParameters(self,numPca,qtdeRecomendacao,usuId,ArquivoId):
        if not numPca:
            return False,'Parâmetro numPca é obrigatório.'
        if not isinstance(numPca,int):
            return False,'Parâmetro numPca deve ser do tipo número inteiro.'
        
        if not qtdeRecomendacao:
            return False,'Parâmetro qtdeRecomendacao é obrigatório.'
        if not isinstance(qtdeRecomendacao,int):
            return False,'Parâmetro qtdeRecomendacao deve ser do tipo número inteiro.'
        if qtdeRecomendacao < 0:
            return False,'Não é possível recomendar 0 camadas de itens.'
        
        if not usuId:
            return False,'Parâmetro usuId é obrigatório.'
        if not isinstance(usuId,int):
            return False,'Parâmetro usuId deve ser do tipo número inteiro.'
        
        if not ArquivoId:
            return False,'Parâmetro arquivoId é obrigatório.'
        
        if not isinstance(ArquivoId,int):
            return False,'Parâmetro arquivoId deve ser do tipo número inteiro.'
        return True,''
    
    def DeleteParameters(self,idParametro):
        Data = Database()
        registerExist = Data.DoSelect(ParametrosTreinamento,APId = idParametro)
        if len(registerExist) == 0:
            return 400,'Não foi encontrado nenhum parâmetro com este ID.'
        response = Data.DoDelete(ParametrosTreinamento,APId = idParametro)
        if response is None:
            return 400,'Ocorreu um erro ao deletar o registro. Tente novamente'
        return 200,''
    
    
    def FindParametersById(self,idParametro):
        Data = Database()
        parametersList = Data.DoSelect(ParametrosTreinamento,APId = idParametro)
        if len(parametersList) == 0:
            return 400,'Não foi encontrado nenhum parâmetro com este ID.',()
        return 200,'',parametersList