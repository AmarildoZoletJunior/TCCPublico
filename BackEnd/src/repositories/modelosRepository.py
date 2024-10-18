from src.repositories.parametrosTreinamentoRepository import ParametrosTreinamentoRepository
from src.data.database import Database
from src.repositories.arquivosProdutosRepository import ArquivosProdutosRepository


class ModelosRepository():
    def __init__(self,data):
        self.Data = data
        
    def RegisterModelOfTraining(self): #Gerar modelo de treinamento unindo todas as informações que existem do dataset
        arquivoId = self.Data.get('arquivoId')
        versao = self.Data.get('versao')
        idUsuario = self.Data.get('idUsuario')
        idParametros = self.Data.get('idParametros')
        
        response,message = self.ValidModel(versao,arquivoId,idUsuario)
        if not response:
            return 400,message
        
        # Verificar a quantidade de produtos que existem no dataset
        arquivosProdRep = ArquivosProdutosRepository()
        response,message,data = arquivosProdRep.FindFileById(arquivoId)
        
        QtdeProdutos = data[0]['APQtdeProdutos']
        if QtdeProdutos < 2:
            return 400,'Não é possível realizar recomendação de produtos com a quantidade de registro inferior a 2 registros.'
        
        parametrosRep = ParametrosTreinamentoRepository()
        response,message,data = parametrosRep.FindParametersById(idParametros)
        if response == 400:
            return 400,message
        
        if data[0]['APIdArquivoProduto'] != arquivoId:
            return 400,'Não é possível treinar um modelo utilizando parametros de outro dataset.'
        
        
        # Aplicar todos os filtros existentes para o dataSet selecionado.
        
        # Verificar a quantidade de registros que ficou após a limpeza do dataset
        
        # Verificar se o dataSet não está vazio.
        
        # Verificar se os parametros passado são compatíveis com o dataset
        
        # Verificar se as variaveis são compativeis com as colunas do dataset, caso falte uma coluna ou tenha uma coluna a mais...não deixar rodar o treinamento (ou rodar apenas com o que existe)
        
        
    def ValidModel(self,MDVersao,MDIdArquivoProd,MDIdUsuario):
        if not MDVersao:
            return False,'A propriedade MDVersao é obrigatória.'
        if not isinstance(MDVersao,str):
            return False,'A propriedade MDVersao aceita apenas valor do tipo texto. Exemplo: 1.0.0.1'
        
        if not MDIdArquivoProd:
            return False,'A propriedade MDIdArquivoProd é obrigatória.'
        if not isinstance(MDIdArquivoProd,int):
            return False,'A propriedade MDIdArquivoProd aceita apenas números inteiro.'
        
        if not MDIdUsuario:
            return False,'A propriedade MDVersao é obrigatória.'
        if not isinstance(MDIdUsuario,int):
            return False,'A propriedade MDIdUsuario aceita apenas números inteiro.'
        
        return True,''

    
    def SelectModelOfTraining():
        print("Aqui ele irá usar o modelo treinado para dar recomendação")
        
        