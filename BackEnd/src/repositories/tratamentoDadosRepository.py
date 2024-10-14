import json
from data.database import Database
from domain.entities.tratamentoDados import TratamentoDados
from domain.enum.tipoDado import TipoDado
from domain.enum.tipoOperacao import OperacaoEnum
from repositories.arquivosProdutosRepository import ArquivosProdutosRepository
from repositories.usuariosRepository import UserRepository
from repositories.variaveisTreinamentosRepository import VariaveisTreinamentoRepository

class TratamentoDadosRepository():
    def __init__(self,data):
        self.Data = data
        
        self.mapa_tipos = {
            1: str,
            2: int,
            3: bool,
            4: float
        }
        
        self.operacao_mapeada = {
            1: 'INSERIR',
            2: 'SUBSTITUIR',
            3: 'REMOVER',
            4: 'DELETAR'
        }

    
    def CreateDataProcessing(self):
        idArquivo = self.Data.get('idArquivo')
        idUsuario = self.Data.get('idUsuario')
        tipoOP = self.Data.get('tipoOP')        
        valorFiltro = self.Data.get('filtros')
        response,message = self.ValidDataProcessing(idArquivo,idUsuario,tipoOP,valorFiltro)
        if response == 400:
            return response,message
        Data = Database()
        response,message = ArquivosProdutosRepository('').FindFileById(idArquivo)
        if response == 400:
            return response,message
        response,message = UserRepository('').FindUserById(idUsuario)
        if response == 400:
            return response,message
        if tipoOP in OperacaoEnum._value2member_map_:
            match tipoOP:
                case 1:#Inserção de valores
                    #{"tipoOP":1,"idArquivo":50,"idUsuario":1,"filtros":[{'campoFiltro':2,'tipoFiltro':1,"valorFiltro":'Abobora'}],"configuracoesAdicionais":{"atributoModificacao":1,"tipoInsercaoDados":1,"valorNovo":'Abobora verde'}} 
                    configuracoesAdicionais = self.Data.get('configuracoesAdicionais')
                    if not isinstance(configuracoesAdicionais, dict):
                        return 400,'Dicionário de configuracoesAdicionais é obrigatório'
                    
                    if not configuracoesAdicionais:
                        return 400,'Parâmetro configuracoesAdicionais é obrigatório'
                    
                    atributoModificacao = configuracoesAdicionais['atributoModificacao']
                    if atributoModificacao is not None:
                        return 400,'Propriedade atributoModificacao da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    tipoInsercaoDados = configuracoesAdicionais['tipoInsercaoDados']
                    if tipoInsercaoDados is not None:
                        return 400,'Propriedade tipoInsercaoDados da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    valorNovo = configuracoesAdicionais['valorNovo']
                    if valorNovo is not None:
                        return 400,'Propriedade valorNovo da propriedade configuracoesAdicionais não foi encontrado.'
                    


                case 2:#Substituição de valores
                    #{"tipoOP":2,"idArquivo":50,"idUsuario":1,"filtros":[{'campoFiltro':2,'tipoFiltro':1,"valorFiltro":'Abobora'}],"configuracoesAdicionais":{"atributoModificacao":1,"ValorAlvo":'Abobora',"valorNovo":'Abobora verde'}} 
                    configuracoesAdicionais = self.Data.get('configuracoesAdicionais')
                    if not isinstance(configuracoesAdicionais, dict):
                        return 400,'Dicionário de configuracoesAdicionais é obrigatório'
                    
                    if not configuracoesAdicionais:
                        return 400,'Parâmetro configuracoesAdicionais é obrigatório'
                    
                    ValorAlvo = configuracoesAdicionais.get(['ValorAlvo'])
                    if ValorAlvo is None:
                        return 400,'Propriedade ValorAlvo da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    atributoModificacao = configuracoesAdicionais.get(['atributoModificacao'])
                    if atributoModificacao is None:
                        return 400,'Propriedade atributoModificacao da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    valorNovo = configuracoesAdicionais.get(['valorNovo'])
                    if valorNovo is None:
                        return 400,'Propriedade valorNovo da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    
                    
                case 3:#Remoção de valores
                    #{"tipoOP":3,"idArquivo":50,"idUsuario":1,"filtros":[{'campoFiltro':2,'tipoFiltro':1,"valorFiltro":'Abobora'}],"configuracoesAdicionais":{"atributoModificacao":1,"ValorRemover":'Abobora verde'}} 
                    configuracoesAdicionais = self.Data.get('configuracoesAdicionais')
                    if not isinstance(configuracoesAdicionais, dict):
                        return 400,'Dicionário de configuracoesAdicionais é obrigatório'
                    
                    if not configuracoesAdicionais:
                        return 400,'Parâmetro configuracoesAdicionais é obrigatório'
                    
                    ValorRemover = configuracoesAdicionais.get(['ValorRemover'])
                    if ValorRemover is None:
                        return 400,'Propriedade ValorRemover da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    atributoModificacao = configuracoesAdicionais.get(['atributoModificacao'])
                    if atributoModificacao is None:
                        return 400,'Propriedade atributoModificacao da propriedade configuracoesAdicionais não foi encontrado.'
                    
                case 4:#Exclusão do registro
                    if len(valorFiltro) > 0:
                        variavelrep = VariaveisTreinamentoRepository('')
                        for valor in valorFiltro:
                            if not valor.get('campoFiltro'):
                                return 400,f'Não foi encontrado o campo que será usado como filtro.'
                            if not valor.get('tipoFiltro'):
                                return 400,f'Não foi encontrado o tipo de filtro que será usado.'
                            if not valor.get('valorFiltro'):
                                return 400,f'Não foi encontrado o valor do filtro que será usado.'
                            response,message,data = variavelrep.FindVariableById(valor['campoFiltro'])
                            if len(data) == 0:
                                return 400, f'Ocorreu um erro ao salvar tratamento de dados, não foi encontrado o campo que será usado como filtro, número do campo: {valor['campoFiltro']}.'
                            status, mensagem = self.comparar_tipo_dado(valor, data[0]['VTTipoDado'])
                            if status == 400:
                                return status,mensagem
                        operacao = self.operacao_mapeada.get(tipoOP)
                        print(valorFiltro)
                        response = Data.DoInsert(TratamentoDados,TDValorFiltro=json.dumps(valorFiltro),TDOperacao=operacao,TDIdArquivoProduto=idArquivo,TDIdUsuario=idUsuario)
                        if response is None:
                            return 400,'Ocorreu um erro ao salvar os dados, tente novamente.'
                        return 200,''
                    else:
                        return 400,f'Não foi encontrado nenhum filtro para realizar a exclusão.'
        else:
            return 400, 'Valor inserido em tipo de operação é inválida'
        
    def comparar_tipo_dado(self,valorFiltro, tipo_dado):
        valor = valorFiltro.get('valorFiltro')
        if tipo_dado.value == TipoDado.int.value:
            tipo_dado = self.mapa_tipos.get(TipoDado.int.value)
            if tipo_dado == type(valor):
                return 200,''
            return 400, "O valor do filtro deve ser do tipo inteiro."
        elif tipo_dado.value == TipoDado.str.value:
            tipo_dado = self.mapa_tipos.get(TipoDado.int.value)
            if tipo_dado == type(valor):
                return 200,''
            return 400, "O valor do filtro deve ser do tipo string."
        elif tipo_dado.value == TipoDado.float.value:
            tipo_dado = self.mapa_tipos.get(TipoDado.int.value)
            if tipo_dado == type(valor):
                return 200,''
            return 400, "O valor do filtro deve ser do tipo float."
        elif tipo_dado.value == TipoDado.bool.value:
            tipo_dado = self.mapa_tipos.get(TipoDado.int.value)
            if tipo_dado == type(valor):
                return 200,''
            return 400, "O valor do filtro deve ser do tipo booleano."
        else:
            return 400,'Tipo não encontrado'
        
        
    def ValidDataProcessing(self,idArquivo,idUsuario,tipoOP,valorFiltro):    
        if not idArquivo:
            return 400,'Parâmetro idArquivo é obrigatório'
        if not idUsuario:
            return 400,'Parâmetro idUsuario é obrigatório'
        if not tipoOP:
            return 400,'Parâmetro tipoOP é obrigatório'
        if not valorFiltro:
            return 400,'Parâmetro filtros é obrigatório'
        return 200,''
        
    def StartDataProcessing(dataSet,arquivoId):
        Data = Database()
        # responseArquivo = Data.DoSelect(ArquivoProdutos,APId=arquivoId)
        # if len(responseArquivo) == 0:
        #     return False,'Não foi encontrado a base de dados dos produto.'
        # responseTratamentoDados = Data.DoSelect(TratamentoDados,TDIdArquivoProduto=arquivoId)
        # if len(responseTratamentoDados) == 0:
        #     return True,'Não existe regra de tratamento de dados ativo.'
        return True,''
    