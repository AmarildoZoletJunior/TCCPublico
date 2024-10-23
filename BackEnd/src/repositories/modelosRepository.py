import io
from src.domain.treatments.MensagemTratamento import MensagemTratamentos


from src.domain.treatments.ErroEntidade import ErroEntidade

from src.repositories.tratamentoDadosRepository import TratamentoDadosRepository
from src.repositories.parametrosTreinamentoRepository import ParametrosTreinamentoRepository
from src.repositories.arquivosProdutosRepository import ArquivosProdutosRepository
from src.repositories.variaveisTreinamentosRepository import VariaveisTreinamentoRepository
from src.domain.enum.tipoOperacao import OperacaoEnum

import json
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors



class ModelosRepository():
    def __init__(self,data):
        self.Data = data
        
        self.mapaTipoDadoInt = {
            1:str,
            2:int,
            3:bool,
            4:float
        }
        
        self.mapaTipoDadoString = {
            str:'Texto',
            int:'Inteiro',
            bool:'Verdadeiro e Falso',
            float:'Número com vírgula'
        }
        
        self.ListaMensagens = []
        
    def RegisterModelOfTraining(self):

        arquivoId = self.Data.get('idArquivo')
        versao = self.Data.get('versao')
        idUsuario = self.Data.get('idUsuario')
        idParametros = self.Data.get('idParametros')
        
        response,message = self.ValidModel(versao,arquivoId,idUsuario,idParametros)
        if not response:
            return 400,message
        
        arquivosProdRep = ArquivosProdutosRepository('')
        response,message,dataArquivo = arquivosProdRep.FindFileById(arquivoId)
        if response == 400:
            return 400,f'Não foi encontrado nenhum dataset de produtos com este id, Id Arquivo:{arquivoId}'

        QtdeProdutos = dataArquivo[0]['APQtdeProdutos']
    
        if QtdeProdutos < 2:
            return 400,'Não é possível realizar recomendação de produtos com a quantidade de registro inferior a 2 registros.'

        dadosArquivo = dataArquivo[0]['APArquivo']
        file_stream = io.BytesIO(dadosArquivo) 
        try:
            DataSet = pd.read_csv(file_stream, delimiter=dataArquivo[0]['APArquivoDelimiter'], encoding='ISO-8859-1')  # Ajuste o encoding conforme necessário
        except pd.errors.ParserError as e:
            return 400, f"Erro ao processar o arquivo CSV que está inserido no banco: {str(e)}, Id Arquivo: {arquivoId}"
        
        parametrosRep = ParametrosTreinamentoRepository('')
        response,message,dataParametro = parametrosRep.FindParametersById(idParametros)
        if response == 400:
            return 400,message
        
        idArquivoParametros = dataParametro[0]['APIdArquivoProduto']
        
        if idArquivoParametros != arquivoId:
            return 400,'Não é possível treinar um modelo utilizando parametros de outro dataset.'
        
        TratamentoDadosRep = TratamentoDadosRepository('')
        dataTratamentos = TratamentoDadosRep.FindDataProcessingByFileId(arquivoId)
        
        if len(dataTratamentos) == 0:
            response = MensagemTratamentos('len(dataTratamentos) == 0','Não foram encontrados nenhum tratamento de dados para este dataset.',"Nenhuma").MontarJson()
            self.ListaMensagens.append(response)

        VariavelRep = VariaveisTreinamentoRepository('')
        dataVariables = VariavelRep.SelectAllVariable()
        if len(dataArquivo) == 0:
            return 400,'Não foi encontrada nenhuma variável(coluna) cadastrada.'
        
        for tratamento in dataTratamentos:
            tipoVariavelString = ''
            FiltroString = ''
            TipoDadoFiltroCorreto = True
            match tratamento['TDOperacao']:
                case OperacaoEnum.INSERIR:
                    tratamentoDados = json.loads(tratamento['TDValorFiltro'])
                    for filtro in tratamentoDados: 
                        VariavelEncontrada = False
                        for variavel in dataVariables:   
                            if filtro['campoFiltro'] == variavel['VTId']:  
                                VariavelEncontrada = True
                                tipoDadoVariavelClasse = self.mapaTipoDadoInt.get(variavel['VTTipoDado'].value)
                                tipoDadoValorFiltroClasse = type(filtro['valorFiltro'])
                                if tipoDadoVariavelClasse == tipoDadoValorFiltroClasse: 
                                    tipoVariavelString = variavel['VTTipoDado'].value
                                    break
                                else:
                                    TipoDadoFiltroCorreto = False
                                    self.ListaMensagens.append(ErroEntidade('TDValorFiltro',f'Foi encontrado um filtro que não condiz com o tipo cadastrado na variável. Tipo da variável: {self.mapaTipoDadoString[tipoDadoVariavelClasse]}, tipo do filtro:{self.mapaTipoDadoString[tipoDadoValorFiltroClasse]}'))
                                    break
                        if not VariavelEncontrada:
                            return 400,f'Não foi encontrado o tipo de dado que é alvo do filtro. Id registro: {tratamento['TDId']}, Id Variável: {filtro['campoFiltro']}'
                        if TipoDadoFiltroCorreto:
                            response,message =  self.CreateFilterString(tipoVariavelString,filtro,dataVariables,tratamento) # tipoVariavelString,filtro,dataVariables
                            if response == 400:
                                return response,message
                            FiltroString = message
                    if TipoDadoFiltroCorreto:
                        modificacaoJson = json.loads(tratamento['TDConfiguracoesAdicionais'])
                        atributoModificacao = modificacaoJson["atributoModificacao"]
                        tipoInsercaoDados = modificacaoJson["tipoInsercaoDados"]
                        valorNovo = modificacaoJson["valorNovo"]
                        if not tipoInsercaoDados:
                            return 400,f'Não foi encontrado o tipo de inserção de dados que será efetuada nos registros, Id do tratamento: {tratamento['TDId']}'
                        
                        if not valorNovo:
                            return 400,f'Não foi encontrado o valor novo que será atribuído aos registros, Id do tratamento: {tratamento['TDId']}'
                        
                        if not atributoModificacao:
                            return 400,f'Não foi encontrado o atributo que será modificado, Id do tratamento: {tratamento['TDId']}'
                        
                        if not isinstance(atributoModificacao,int):
                            return False,f'A propriedade atributoModificacao aceita apenas números inteiro. Id do tratamento: {tratamento['TDId']}'
                        
                        if not isinstance(tipoInsercaoDados,int):
                            return False,f'A propriedade tipoInsercaoDados aceita apenas números inteiro. Id do tratamento: {tratamento['TDId']}'
                        for variavel in dataVariables:   
                            if atributoModificacao == variavel['VTId']:  
                                tipoDadoVariavelClasse = self.mapaTipoDadoInt.get(variavel['VTTipoDado'].value)
                                tipoDadoValorMudancaDados = type(valorNovo)
                                if tipoDadoValorMudancaDados != tipoDadoVariavelClasse:
                                    return False,f'A propriedade valorNovo não tem o mesmo tipo de dado que a variável que será atualizada. Id do tratamento: {tratamento['TDId']}, tipo dado valorNovo: {self.mapaTipoDadoString[tipoDadoValorMudancaDados]}, id da variável: {variavel['VTId']},tipo dado variável: {self.mapaTipoDadoString[tipoDadoVariavelClasse]}'
                                if tipoDadoVariavelClasse == int:
                                    return 400, f'Não é possível fazer inserção de valores em coluna do tipo inteiro. Id tratamento: {tratamento['TDId']}'
                                elif tipoDadoVariavelClasse == float:
                                    return 400, f'Não é possível fazer inserção de valores em coluna do tipo número com vírgula. Id tratamento: {tratamento['TDId']}'
                                elif tipoDadoVariavelClasse == bool:
                                    return 400, f'Não é possível fazer inserção de valores em coluna do tipo verdadeiro/falso. Id tratamento: {tratamento['TDId']}'
                                else:
                                    try:
                                        filtrado = eval(FiltroString) 
                                        match tipoInsercaoDados:
                                            case 1:
                                                DataSet.loc[filtrado, variavel['VTNome']] = str(valorNovo) + " " + DataSet.loc[filtrado, variavel['VTNome']] 
                                            case 2:
                                                DataSet.loc[filtrado, variavel['VTNome']] = DataSet.loc[filtrado, variavel['VTNome']] + " " + str(valorNovo)
                                            case _:
                                                return 400,f'Não foi encontrado qual tipo de inserção que deseja fazer em registros. Id tratamento: {tratamento['TDId']}'
                                        response = MensagemTratamentos(FiltroString,len(DataSet[filtrado]),"Inserir").MontarJson()
                                        self.ListaMensagens.append(response)
                                        break
                                    except Exception as error:
                                        return 400,f'Ocorreu um erro ao executar um tratamento de dados. Id tratamento: {tratamento['TDId']}, erro:{error}'
                        return 200,self.ListaMensagens
                    
                case OperacaoEnum.SUBSTITUIR:
                    print('2')
                    tratamentoDados = json.loads(tratamento['TDValorFiltro'])
                    FiltroComando = ''
                    for filtro in tratamentoDados:
                        match filtro['tipoFiltro']:
                            case 1:
                                FiltroComando += '(DataSet[''])'
                                print()
                            case 2:
                                print()
                            case 3:
                                print()
                            case 4:
                                print()
                            case 5: 
                                print()
                case OperacaoEnum.REMOVER:
                    print('3')
                    FiltroComando = ''
                    tratamentoDados = json.loads(tratamento['TDValorFiltro'])
                    for filtro in tratamentoDados:
                        match filtro['tipoFiltro']:
                            case 1:
                                print()
                            case 2:
                                print()
                            case 3:
                                print()
                            case 4:
                                print()
                            case 5: 
                                print()
                case OperacaoEnum.DELETAR:
                    tipoVariavelString = ''
                    tratamentoDados = json.loads(tratamento['TDValorFiltro'])
                    for filtro in tratamentoDados: 
                        VariavelEncontrada = False
                        for variavel in dataVariables:   
                            if filtro['campoFiltro'] == variavel['VTId']:  
                                VariavelEncontrada = True
                                tipoDadoVariavelClasse = self.mapaTipoDadoInt.get(variavel['VTTipoDado'].value)
                                tipoDadoValorFiltroClasse = type(filtro['valorFiltro'])
                                if tipoDadoVariavelClasse == tipoDadoValorFiltroClasse:
                                    tipoVariavelString = variavel['VTTipoDado'].value
                                    break
                                else:
                                    TipoDadoFiltroCorreto = False
                                    self.ListaMensagens.append(ErroEntidade('TDValorFiltro',f'Foi encontrado um filtro que não condiz com o tipo cadastrado na variável. Tipo da variável: {self.mapaTipoDadoString[tipoDadoVariavelClasse]}, tipo do filtro:{self.mapaTipoDadoString[tipoDadoValorFiltroClasse]}'))
                                    break
                        if not VariavelEncontrada:
                            return 400,f'Não foi encontrado o tipo de dado que é alvo do filtro. Id registro: {tratamento['TDId']}, Id Variável: {filtro['campoFiltro']}'
                        if TipoDadoFiltroCorreto:
                            response,message =  self.CreateFilterString(tipoVariavelString,filtro,dataVariables,tratamento) # tipoVariavelString,filtro,dataVariables
                            if response == 400:
                                return response,message
                            FiltroString = message
                    if TipoDadoFiltroCorreto:
                        filtrado = eval(FiltroString)
                        try:
                            DataSet.drop(DataSet[filtrado].index,inplace=True)
                            response = MensagemTratamentos(FiltroString,len(DataSet[filtrado]),"Deletar").MontarJson()
                            self.ListaMensagens.append(response) 
                        except Exception as error:
                            return 400,f'Ocorreu um erro ao executar um tratamento de dados. Id tratamento: {tratamento['TDId']}, erro:{error}'
                    
        return 200,'Ok'


        
        # Aplicar todos os filtros existentes para o dataSet selecionado.
        
        # Verificar a quantidade de registros que ficou após a limpeza do dataset
        
        # Verificar se o dataSet não está vazio.
        
        # Verificar se os parametros passado são compatíveis com o dataset
        
        # Verificar se as variaveis são compativeis com as colunas do dataset, caso falte uma coluna ou tenha uma coluna a mais...não deixar rodar o treinamento (ou rodar apenas com o que existe)
        
        
    def ValidModel(self,MDVersao,MDIdArquivoProd,MDIdUsuario,MDIdParametros):
        if not MDVersao:
            return False,'A propriedade versao é obrigatória.'
        if not isinstance(MDVersao,str):
            return False,'A propriedade versao aceita apenas valor do tipo texto. Exemplo: 1.0.0.1'
        
        if not MDIdArquivoProd:
            return False,'A propriedade idArquivo é obrigatória.'
        if not isinstance(MDIdArquivoProd,int):
            return False,'A propriedade idArquivo aceita apenas números inteiro.'
        
        if not MDIdUsuario:
            return False,'A propriedade idUsuario é obrigatória.'
        if not isinstance(MDIdUsuario,int):
            return False,'A propriedade idUsuario aceita apenas números inteiro.'
        
        if not MDIdParametros:
            return False,'A propriedade idParametros é obrigatória.'
        if not isinstance(MDIdParametros,int):
            return False,'A propriedade idParametros aceita apenas números inteiro.'
        
        return True,''
    
    
    def TrainingKNN(numPca,QtdeRecomendacao,dataSet):
        #Preciso iterar sobre todas as variaveis, e ir distribuindo os tratamentos conforme o tipo de dado
        
        
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(dataSet['DescricaoProduto'])

        pca = PCA(n_components=numPca)
        tfidf_reduced = pca.fit_transform(tfidf_matrix.toarray())

        # categorical_features = DataSet[['CodDepartamento', 'CodSecao']]
        # encoder = OneHotEncoder(sparse_output=False)
        # encoded_categorical = encoder.fit_transform(categorical_features)

        # self.combined_features = np.hstack([tfidf_reduced, encoded_categorical])

        # self.model = NearestNeighbors(n_neighbors=QtdeRecomendacao + 1, metric='nan_euclidean') 

        # self.model.fit(self.combined_features)
        
        
    def CreateFilterString(self,tipoVariavelString,filtro,dataVariables,tratamento):
        match tipoVariavelString:
            case 1:
                match filtro['tipoFiltro']:
                        case 1:
                            for variavel in dataVariables:   
                                if filtro['campoFiltro'] == variavel['VTId']:
                                    if len(FiltroString) == 0:
                                        FiltroString = fr'DataSet["{variavel['VTNome']}"].str.contains(\b{filtro['valorFiltro']}\b,case=False,regex=True)'
                                    else:
                                        FiltroString += fr' && DataSet["{variavel['VTNome']}"].str.contains(\b{filtro['valorFiltro']}\b,case=False,regex=True)'
                                    return 200,FiltroString
                        case 2:
                            for variavel in dataVariables:   
                                if filtro['campoFiltro'] == variavel['VTId']:  
                                    if len(FiltroString) == 0:
                                        FiltroString = fr'DataSet["{variavel['VTNome']}"] == {filtro['valorFiltro']}'
                                    else:
                                        FiltroString += fr' && DataSet["{variavel['VTNome']}"] == {filtro['valorFiltro']}'
                                    return 200,FiltroString
                        case 3:
                            for variavel in dataVariables:   
                                if filtro['campoFiltro'] == variavel['VTId']:  
                                    if len(FiltroString) == 0:
                                        FiltroString = fr'DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True)'
                                    else:
                                        FiltroString += fr' && DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True)'
                                    return 200,FiltroString
                        case 4:
                            for variavel in dataVariables:
                                if filtro['campoFiltro'] == variavel['VTId']:  
                                    if len(FiltroString) == 0:
                                        FiltroString = fr'DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True)'
                                    else:
                                        FiltroString += fr' && DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True)'
                                    return 200,FiltroString
                        case 5: 
                            for variavel in dataVariables:   
                                if filtro['campoFiltro'] == variavel['VTId']:  
                                    if len(FiltroString) == 0:
                                        FiltroString = fr'DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True)'
                                    else:
                                        FiltroString += fr' && DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True)'
                                    return 200,FiltroString 
                        case _:
                            return 400,f'Não foi encontrado o tipo de filtro cadastrado, Id tratamento: {tratamento['TDId']}'
            case 2:
                for variavel in dataVariables:   
                    if filtro['campoFiltro'] == variavel['VTId']:  
                        FiltroString = fr'DataSet["{variavel['VTNome']}"] == {filtro['valorFiltro']}'
                return 200,FiltroString
                
            case 3:
                print('Caiu bool') #Analisar como irá vir
                return 200,''
                
            case 4:
                for variavel in dataVariables:   
                    if filtro['campoFiltro'] == variavel['VTId']:  
                        FiltroString = fr'DataSet["{variavel['VTNome']}"] == {filtro['valorFiltro']}'
                return 200,FiltroString
            case _:
                return 400, f'Não foi encontrado o tipo de dado cadastrado, Id tratamento: {tratamento['TDId']}'
            
            
    def ValidationFilterData(self,dataVariables,filtro):
        for variavel in dataVariables:   
            if filtro['campoFiltro'] == variavel['VTId']:  
                VariavelEncontrada = True
                tipoDadoVariavelClasse = self.mapaTipoDadoInt.get(variavel['VTTipoDado'].value)
                tipoDadoValorFiltroClasse = type(filtro['valorFiltro'])
                if tipoDadoVariavelClasse == tipoDadoValorFiltroClasse:
                    tipoVariavelString = variavel['VTTipoDado'].value
                    break
                else:
                    TipoDadoFiltroCorreto = False
                    self.ListaMensagens.append(ErroEntidade('TDValorFiltro',f'Foi encontrado um filtro que não condiz com o tipo cadastrado na variável. Tipo da variável: {self.mapaTipoDadoString[tipoDadoVariavelClasse]}, tipo do filtro:{self.mapaTipoDadoString[tipoDadoValorFiltroClasse]}'))
                    break