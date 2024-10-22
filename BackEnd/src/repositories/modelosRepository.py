

import json
from src.domain.error.ErroEntidade import ErroEntidade
from src.repositories.tratamentoDadosRepository import TratamentoDadosRepository
from src.repositories.parametrosTreinamentoRepository import ParametrosTreinamentoRepository
from src.repositories.arquivosProdutosRepository import ArquivosProdutosRepository
from src.repositories.variaveisTreinamentosRepository import VariaveisTreinamentoRepository
from src.domain.enum.tipoOperacao import OperacaoEnum

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
        
        self.ListaMensagemErro = []
    
        
    def RegisterModelOfTraining(self): #Gerar modelo de treinamento unindo todas as informações que existem do dataset
        ListaMensagem = []
        arquivoId = self.Data.get('idArquivo')
        versao = self.Data.get('versao')
        idUsuario = self.Data.get('idUsuario')
        idParametros = self.Data.get('idParametros')
        
        response,message = self.ValidModel(versao,arquivoId,idUsuario,idParametros)
        if not response:
            return 400,message
        
        # Verificar a quantidade de produtos que existem no dataset
        arquivosProdRep = ArquivosProdutosRepository('')
        response,message,data = arquivosProdRep.FindFileById(arquivoId)
        
        QtdeProdutos = data[0]['APQtdeProdutos']
        
        if QtdeProdutos < 2:
            return 400,'Não é possível realizar recomendação de produtos com a quantidade de registro inferior a 2 registros.'
        
        parametrosRep = ParametrosTreinamentoRepository('')
        response,message,data = parametrosRep.FindParametersById(idParametros)
        if response == 400:
            return 400,message
        
        idArquivoParametros = data[0]['APIdArquivoProduto']
        
        if idArquivoParametros != arquivoId:
            return 400,'Não é possível treinar um modelo utilizando parametros de outro dataset.'
        
        TratamentoDadosRep = TratamentoDadosRepository('')
        data = TratamentoDadosRep.FindDataProcessingByFileId(arquivoId)
        
        if len(data) == 0:
            ListaMensagem.append('Não foram encontrados nenhum tratamento de dados para este dataset.')


        VariavelRep = VariaveisTreinamentoRepository('')
        dataVariables = VariavelRep.SelectAllVariable()
        if len(data) == 0:
            return 400,'Não foi encontrada nenhuma variável(coluna) cadastrada.'
        
        erroEntidade = ErroEntidade()
        for tratamento in data:
            FiltroString = ''
            filtroCorreto = True
            match tratamento['TDOperacao']:
                case OperacaoEnum.INSERIR:
                    tratamentoDados = json.loads(tratamento['TDValorFiltro'])
                    for filtro in tratamentoDados: #Itera sobre todos os filtros aplicados para esta ação
                        for variavel in dataVariables:   
                            VariavelEncontrada = False #Flag
                            if filtro['campoFiltro'] == variavel['VTId']:  
                                VariavelEncontrada = True  #Se encontrar, ele marca a flag
                                tipoDadoVariavelClasse = self.mapaTipoDadoInt.get(variavel['VTTipoDado'].value)
                                tipoDadoValorFiltroClasse = type(filtro['valorFiltro'])
                                if tipoDadoVariavelClasse == tipoDadoValorFiltroClasse: #Compara se o tipo de dado dela é compatível com o tipo de dado cadastrado nas viriaveis do banco.
                                    break
                                else:
                                    filtroCorreto = False
                                    erroEntidade.AdicionarMensagem('TDValorFiltro',f'Foi encontrado um filtro que não condiz com o tipo cadastrado na variável. Tipo da variável: {self.mapaTipoDadoString[tipoDadoVariavelClasse]}, tipo do filtro:{self.mapaTipoDadoString[tipoDadoValorFiltroClasse]}')
                                    break
                        if not VariavelEncontrada:
                            return 400,f'Não foi encontrado o tipo de dado que é alvo do filtro. Id registro: {tratamento['TDId']}, Id Variável: {filtro['campoFiltro']}'
                        if filtroCorreto: #Monta a string de filtro para pegar somente registros que deseja
                            match filtro['tipoFiltro']:
                                case 1:
                                    for variavel in dataVariables:   
                                        if filtro['campoFiltro'] == variavel['VTId']:  
                                            if len(FiltroString) == 0:
                                                FiltroString = fr'(self.DataSet["{variavel['VTNome']}"].str.contains(\b{filtro['valorFiltro']}\b,case=False,regex=True))'
                                            else:
                                                FiltroString += fr' && (self.DataSet["{variavel['VTNome']}"].str.contains(\b{filtro['valorFiltro']}\b,case=False,regex=True))'
                                            break
                                case 2:
                                    for variavel in dataVariables:   
                                        if filtro['campoFiltro'] == variavel['VTId']:  
                                            if len(FiltroString) == 0:
                                                FiltroString = fr'(self.DataSet["{variavel['VTNome']}"] == {filtro['valorFiltro']})'
                                            else:
                                                FiltroString += fr' && (self.DataSet["{variavel['VTNome']}"] == {filtro['valorFiltro']})'
                                            break
                                case 3:
                                    for variavel in dataVariables:   
                                        if filtro['campoFiltro'] == variavel['VTId']:  
                                            if len(FiltroString) == 0:
                                                FiltroString = fr'(self.DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True))'
                                            else:
                                                FiltroString += fr' && (self.DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True))'
                                            break
                                case 4:
                                    for variavel in dataVariables:
                                        if filtro['campoFiltro'] == variavel['VTId']:  
                                            if len(FiltroString) == 0:
                                                FiltroString = fr'(self.DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True))'
                                            else:
                                                FiltroString += fr' && (self.DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True))'
                                            break
                                case 5: 
                                    for variavel in dataVariables:   
                                        if filtro['campoFiltro'] == variavel['VTId']:  
                                            if len(FiltroString) == 0:
                                                FiltroString = fr'(self.DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True))'
                                            else:
                                                FiltroString += fr' && (self.DataSet["{variavel['VTNome']}"].str.contains({filtro['valorFiltro']}\b,case=False,regex=True))'
                                            break
                    print(FiltroString)
                    if filtroCorreto:
                        # {"atributoModificacao": 1, "tipoInsercaoDados": 1, "valorNovo": 1}
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
                                    match tipoInsercaoDados: #Aqui monta tipo de inserção de dados
                                        case 1:
                                            print('Aqui caiu InserirComeco')
                                        case 2:
                                            print('Aqui caiu InserirFim')
                                    break

                case OperacaoEnum.SUBSTITUIR:
                    print('2')
                    tratamentoDados = json.loads(tratamento['TDValorFiltro'])
                    FiltroComando = ''
                    for filtro in tratamentoDados:
                        
                        match filtro['tipoFiltro']:
                            case 1:
                                FiltroComando += '(self.DataSet[''])'
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
                    print('4')
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
                    
            
            
        # Contem = 1
        # Igual = 2
        # Inicia = 3
        # Finaliza = 4
        # NaoContem = 5
        
        
        
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

    
    def SelectModelOfTraining():
        print("Aqui ele irá usar o modelo treinado para dar recomendação")
        
        