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
                    operacao = self.operacao_mapeada.get(tipoOP)
                    
                    if not configuracoesAdicionais:
                        return 400,'Parâmetro configuracoesAdicionais é obrigatório'
                    
                    if not isinstance(configuracoesAdicionais, dict):
                        return 400,'Dicionário de configuracoesAdicionais é obrigatório'
                    
                    atributoModificacao = configuracoesAdicionais.get('atributoModificacao')
                    if atributoModificacao is None:
                        return 400,'Propriedade atributoModificacao da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    tipoInsercaoDados = configuracoesAdicionais.get('tipoInsercaoDados')
                    if tipoInsercaoDados is None:
                        return 400,'Propriedade tipoInsercaoDados da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    if not isinstance(tipoInsercaoDados, int):
                        return 400,'O tipoInsercaoDados deve ser do tipo inteiro.'

                    valorNovo = configuracoesAdicionais.get('valorNovo')
                    if valorNovo is None:
                        return 400,'Propriedade valorNovo da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    configuracoesAdicionaisJson = json.dumps(configuracoesAdicionais)
                    QtdeFiltros = len(valorFiltro)
                    if QtdeFiltros > 0:
                        valorFiltroJson = json.dumps(valorFiltro)
                        response,message = self.FindDataProcessingByAdditionalFilter(idArquivo,valorFiltroJson,operacao)
                        if response == 400:
                                return response,message
                        variavelrep = VariaveisTreinamentoRepository('')
                        for valor in valorFiltro:
                            # region verificação campo Filtro
                            if not valor.get('campoFiltro'):
                                return 400,f'Não foi encontrado o campo que será usado como filtro.'
                            if not isinstance(valor.get('campoFiltro'), int):
                                return 400,f'O campoFiltro deve ser do tipo inteiro.'
                            response,message,data = variavelrep.FindVariableById(valor['campoFiltro'])
                            if response == 400:
                                return response, f'Ocorreu um erro ao salvar tratamento de dados, não foi encontrado o campo que será usado como filtro, número do campo: {valor['campoFiltro']}.'
                            # endregion       
                            # region verificação campo tipoFiltro
                            if not valor.get('tipoFiltro'):
                                return 400,f'Não foi encontrado o tipo de filtro que será usado.'
                            if not isinstance(valor.get('tipoFiltro'), int):
                                return 400,f'O tipoFiltro deve ser do tipo inteiro.'
                            #endregion
                            # region verificação campo valorFiltro
                            if not valor.get('valorFiltro'):
                                return 400,f'Não foi encontrado o valor do filtro que será usado.'
                            #endregion
                            response, message = self.CompararTipoDado(valor['valorFiltro'], data[0]['VTTipoDado'],'valorFiltro')
                            if response == 400:
                                return response,message  
                            
                                         
                        response,message,data = variavelrep.FindVariableById(atributoModificacao)
                        if response == 400:
                                return response, f'Ocorreu um erro ao salvar tratamento de dados, não foi encontrado o campo que será usado como atributo a ser modificado, número do campo: {atributoModificacao}.'
                        response, message = self.CompararTipoDado(valorNovo, data[0]['VTTipoDado'],'valorNovo')
                        if response == 400:
                                return response,message
                        response,message = self.FindDataProcessingByAdditionalFilter(idArquivo,configuracoesAdicionaisJson,operacao)
                        if response == 400:
                            return response,message     
                        response = Data.DoInsert(TratamentoDados,TDValorFiltro=valorFiltroJson,TDOperacao=operacao,TDIdArquivoProduto=idArquivo,TDIdUsuario=idUsuario,TDConfiguracoesAdicionais = configuracoesAdicionaisJson)
                        if response is None:
                            return 400,'Ocorreu um erro ao salvar os dados, tente novamente.'
                        return 200,''
                    else:
                        response,message,data = variavelrep.FindVariableById(atributoModificacao)
                        if response == 400:
                                return response, f'Ocorreu um erro ao salvar tratamento de dados, não foi encontrado o campo que será usado como atributo a ser modificado, número do campo: {atributoModificacao}.'
                        response, message = self.CompararTipoDado(valorNovo, data[0]['VTTipoDado'],'valorNovo')
                        if response == 400:
                                return response,message
                        response,message = self.FindDataProcessingByAdditionalFilter(idArquivo,configuracoesAdicionaisJson,operacao)
                        if response == 400:
                            return response,message     
                        response = Data.DoInsert(TratamentoDados,TDValorFiltro=valorFiltroJson,TDOperacao=operacao,TDIdArquivoProduto=idArquivo,TDIdUsuario=idUsuario,TDConfiguracoesAdicionais = configuracoesAdicionaisJson)
                        if response is None:
                            return 400,'Ocorreu um erro ao salvar os dados, tente novamente.'
                        return 200,''

                case 2:#Substituição de valores
                    #{"tipoOP":2,"idArquivo":50,"idUsuario":1,"filtros":[{'campoFiltro':2,'tipoFiltro':1,"valorFiltro":'Abobora'}],"configuracoesAdicionais":{"atributoModificacao":1,"ValorAlvo":'Abobora',"valorNovo":'Abobora verde'}} 
                    operacao = self.operacao_mapeada.get(tipoOP)

                    configuracoesAdicionais = self.Data.get('configuracoesAdicionais')
                    if not isinstance(configuracoesAdicionais, dict):
                        return 400,'Dicionário de configuracoesAdicionais é obrigatório'
                    
                    if not configuracoesAdicionais:
                        return 400,'Parâmetro configuracoesAdicionais é obrigatório'
                    
                    ValorAlvo = configuracoesAdicionais.get('ValorAlvo')
                    if ValorAlvo is None:
                        return 400,'Propriedade ValorAlvo da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    atributoModificacao = configuracoesAdicionais.get('atributoModificacao')
                    if atributoModificacao is None:
                        return 400,'Propriedade atributoModificacao da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    valorNovo = configuracoesAdicionais.get('valorNovo')
                    if valorNovo is None:
                        return 400,'Propriedade valorNovo da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    configuracoesAdicionaisJson = json.dumps(configuracoesAdicionais)
                    QtdeFiltros = len(valorFiltro)
                    if QtdeFiltros > 0:
                        valorFiltroJson = json.dumps(valorFiltro)
                        response,message = self.FindDataProcessingByFilterValue(idArquivo,valorFiltroJson,operacao)
                        if response == 400:
                                return response,message
                        variavelrep = VariaveisTreinamentoRepository('')
                        for valor in valorFiltro:
                            # region verificação campo Filtro
                            if not valor.get('campoFiltro'):
                                return 400,f'Não foi encontrado o campo que será usado como filtro.'
                            if not isinstance(valor.get('campoFiltro'), int):
                                return 400,f'O campoFiltro deve ser do tipo inteiro.'
                            response,message,data = variavelrep.FindVariableById(valor['campoFiltro'])
                            if response == 400:
                                return response, f'Ocorreu um erro ao salvar tratamento de dados, não foi encontrado o campo que será usado como filtro, número do campo: {valor['campoFiltro']}.'
                            # endregion       
                            # region verificação campo tipoFiltro
                            if not valor.get('tipoFiltro'):
                                return 400,f'Não foi encontrado o tipo de filtro que será usado.'
                            if not isinstance(valor.get('tipoFiltro'), int):
                                return 400,f'O tipoFiltro deve ser do tipo inteiro.'
                            #endregion
                            # region verificação campo valorFiltro
                            if not valor.get('valorFiltro'):
                                return 400,f'Não foi encontrado o valor do filtro que será usado.'
                            #endregion
                            response, message = self.CompararTipoDado(valor.get('valorFiltro'), data[0]['VTTipoDado'],'valorFiltro')
                            if response == 400:
                                return response,message 
                                         
                        response,message,data = variavelrep.FindVariableById(atributoModificacao)
                        if response == 400:
                                return response, f'Ocorreu um erro ao salvar tratamento de dados, não foi encontrado o campo que será usado como atributo a ser modificado, número do campo: {atributoModificacao}.'
                            
                        response, message = self.CompararTipoDado(ValorAlvo, data[0]['VTTipoDado'],'ValorAlvo')
                        if response == 400:
                                return response,message
                        response, message = self.CompararTipoDado(valorNovo, data[0]['VTTipoDado'],'ValorNovo')
                        if response == 400:
                                return response,message
                        response,message = self.FindDataProcessingByAdditionalFilter(idArquivo,configuracoesAdicionaisJson,operacao)
                        if response == 400:
                            return response,message     
                        response = Data.DoInsert(TratamentoDados,TDValorFiltro=valorFiltroJson,TDOperacao=operacao,TDIdArquivoProduto=idArquivo,TDIdUsuario=idUsuario,TDConfiguracoesAdicionais = configuracoesAdicionaisJson)
                        if response is None:
                            return 400,'Ocorreu um erro ao salvar os dados, tente novamente.'
                        return 200,''
                    else:

                        response,message,data = variavelrep.FindVariableById(atributoModificacao)
                        if response == 400:
                                return response, f'Ocorreu um erro ao salvar tratamento de dados, não foi encontrado o campo que será usado como atributo a ser modificado, número do campo: {atributoModificacao}.'
                        response, message = self.CompararTipoDado(ValorAlvo, data[0]['VTTipoDado'],'valorAlvo')
                        if response == 400:
                                return response,message
                        response, message = self.CompararTipoDado(valorNovo, data[0]['VTTipoDado'],'valorNovo')
                        if response == 400:
                                return response,message
                        response,message = self.FindDataProcessingByAdditionalFilter(idArquivo,configuracoesAdicionaisJson,operacao)
                        if response == 400:
                            return response,message     
                        response = Data.DoInsert(TratamentoDados,TDValorFiltro=valorFiltroJson,TDOperacao=operacao,TDIdArquivoProduto=idArquivo,TDIdUsuario=idUsuario,TDConfiguracoesAdicionais = configuracoesAdicionaisJson)
                        if response is None:
                            return 400,'Ocorreu um erro ao salvar os dados, tente novamente.'
                        return 200,''
                    
                case 3:#Remoção de valores
                    #{"tipoOP":3,"idArquivo":50,"idUsuario":1,"filtros":[{'campoFiltro':2,'tipoFiltro':1,"valorFiltro":'Abobora'}],"configuracoesAdicionais":{"atributoModificacao":1,"ValorRemover":'Abobora verde'}} 
                    operacao = self.operacao_mapeada.get(tipoOP)
                    configuracoesAdicionais = self.Data.get('configuracoesAdicionais')
                    if not configuracoesAdicionais:
                        return 400,'Parâmetro configuracoesAdicionais é obrigatório'
                    
                    if not isinstance(configuracoesAdicionais, dict):
                        return 400,'Dicionário de configuracoesAdicionais é obrigatório'
                    
                    ValorRemover = configuracoesAdicionais.get('ValorRemover')
                    if ValorRemover is None:
                        return 400,'Propriedade ValorRemover da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    atributoModificacao = configuracoesAdicionais.get('atributoModificacao')
                    if atributoModificacao is None:
                        return 400,'Propriedade atributoModificacao da propriedade configuracoesAdicionais não foi encontrado.'
                    
                    if not isinstance(atributoModificacao,int):
                        return 400,f'O atributoModificacao deve ser do tipo inteiro.'
                    
                    configuracoesAdicionaisJson = json.dumps(configuracoesAdicionais)
                    QtdeFiltros = len(valorFiltro)
                    if QtdeFiltros > 0:
                        
                        valorFiltroJson = json.dumps(valorFiltro)
                        variavelrep = VariaveisTreinamentoRepository('')
                        for valor in valorFiltro:
                            # region verificação campo Filtro
                            if not valor.get('campoFiltro'):
                                return 400,f'Não foi encontrado o campo que será usado como filtro.'
                            if not isinstance(valor.get('campoFiltro'), int):
                                return 400,f'O campoFiltro deve ser do tipo inteiro.'
                            response,message,data = variavelrep.FindVariableById(valor['campoFiltro'])
                            if response == 400:
                                return response, f'Ocorreu um erro ao salvar tratamento de dados, não foi encontrado o campo que será usado como filtro, número do campo: {valor['campoFiltro']}.'
                            # endregion       
                            # region verificação campo tipoFiltro
                            if not valor.get('tipoFiltro'):
                                return 400,f'Não foi encontrado o tipo de filtro que será usado.'
                            if not isinstance(valor.get('tipoFiltro'), int):
                                return 400,f'O tipoFiltro deve ser do tipo inteiro.'
                            #endregion
                            # region verificação campo valorFiltro
                            if not valor.get('valorFiltro'):
                                return 400,f'Não foi encontrado o valor do filtro que será usado.'
                            #endregion
                            response, message = self.CompararTipoDado(valor['valorFiltro'], data[0]['VTTipoDado'],'valorFiltro')
                            if response == 400:
                                return response,message   
                        response,message,data = variavelrep.FindVariableById(atributoModificacao)
                        if response == 400:
                                return response, f'Ocorreu um erro ao salvar tratamento de dados, não foi encontrado o campo que será usado como atributo a ser modificado, número do campo: {atributoModificacao}.'
                        response, message = self.CompararTipoDado(ValorRemover, data[0]['VTTipoDado'],'ValorRemover')
                        if response == 400:
                                return response,message
                        response,message = self.FindDataProcessingByAdditionalFilter(idArquivo,configuracoesAdicionaisJson,operacao)
                        if response == 400:
                            return response,message     
                        response = Data.DoInsert(TratamentoDados,TDValorFiltro=valorFiltroJson,TDOperacao=operacao,TDIdArquivoProduto=idArquivo,TDIdUsuario=idUsuario,TDConfiguracoesAdicionais = configuracoesAdicionaisJson)
                        if response is None:
                            return 400,'Ocorreu um erro ao salvar os dados, tente novamente.'
                        return 200,''
                    else:
                        
                        variavelrep = VariaveisTreinamentoRepository('')
                        
                        response,message,data = variavelrep.FindVariableById(atributoModificacao)
                        if response == 400:
                                return response, f'Ocorreu um erro ao salvar tratamento de dados, não foi encontrado o campo que será usado como filtro, número do campo: {atributoModificacao}.'
                        response, message = self.CompararTipoDado(ValorRemover, data[0]['VTTipoDado'],'ValorRemover')
                        if response == 400:
                                return response,message    
                        response,message = self.FindDataProcessingByAdditionalFilter(idArquivo,configuracoesAdicionaisJson,operacao)
                        if response == 400:
                            return response,message
                        
                        response = Data.DoInsert(TratamentoDados,TDOperacao=operacao,TDIdArquivoProduto=idArquivo,TDIdUsuario=idUsuario,TDConfiguracoesAdicionais = configuracoesAdicionaisJson)
                        if response is None:
                            return 400,'Ocorreu um erro ao salvar os dados, tente novamente.'
                        return 200,''
                    
                case 4:#Exclusão do registro
                    QtdeFiltros = len(valorFiltro)
                    if QtdeFiltros > 0:
                        variavelrep = VariaveisTreinamentoRepository('')
                        for valor in valorFiltro: 
                            # region verificação campo Filtro
                            if not valor.get('campoFiltro'):
                                return 400,f'Não foi encontrado o campo que será usado como filtro.'
                            if not isinstance(valor.get('campoFiltro'), int):
                                return 400,f'O campoFiltro deve ser do tipo inteiro.'
                            response,message,data = variavelrep.FindVariableById(valor['campoFiltro'])
                            if response == 400:
                                return response, f'Ocorreu um erro ao salvar tratamento de dados, não foi encontrado o campo que será usado como filtro, número do campo: {valor['campoFiltro']}.'
                            #endregion   
                            # region verificação campo tipoFiltro
                            if not valor.get('tipoFiltro'):
                                return 400,f'Não foi encontrado o tipo de filtro que será usado.'
                            if not isinstance(valor.get('tipoFiltro'), int):
                                return 400,f'O tipoFiltro deve ser do tipo inteiro.'
                            #endregion
                            # region verificação campo valorFiltro
                            if not valor.get('valorFiltro'):
                                return 400,f'Não foi encontrado o valor do filtro que será usado.'
                            status, mensagem = self.CompararTipoDado(valor.get('valorFiltro'), data[0]['VTTipoDado'],'valorFiltro')
                            if status == 400:
                                return status,mensagem
                            #endregion    
                        operacao = self.operacao_mapeada.get(tipoOP)
                        valorFiltroJson = json.dumps(valorFiltro)
                        response,message = self.FindDataProcessingByFilterValue(idArquivo,valorFiltroJson,operacao)
                        if response == 400:
                                return response,message
                        response = Data.DoInsert(TratamentoDados,TDValorFiltro=valorFiltroJson,TDOperacao=operacao,TDIdArquivoProduto=idArquivo,TDIdUsuario=idUsuario)
                        if response is None:
                            return 400,'Ocorreu um erro ao salvar os dados, tente novamente.'
                        return 200,''
                    else:
                        return 400,f'Não foi encontrado nenhum filtro para realizar a exclusão.'
        else:
            return 400, 'Valor inserido em tipo de operação é inválida'
        
        
    def CompararTipoDado(self,valorFiltro, tipo_dado,nomeJsonVariavel):
        valor = valorFiltro
        if tipo_dado.value == TipoDado.int.value:
            tipo_dado = self.mapa_tipos.get(TipoDado.int.value)
            if tipo_dado == type(valor):
                return 200,''
            return 400, f"O valor da propriedade {nomeJsonVariavel} deve ser do tipo inteiro."
        elif tipo_dado.value == TipoDado.str.value:
            tipo_dado = self.mapa_tipos.get(TipoDado.str.value)
            if tipo_dado == type(valor):
                return 200,''
            return 400, f"O valor da propriedade {nomeJsonVariavel} deve ser do tipo string."
        elif tipo_dado.value == TipoDado.float.value:
            tipo_dado = self.mapa_tipos.get(TipoDado.float.value)
            if tipo_dado == type(valor):
                return 200,''
            return 400, f"O valor da propriedade {nomeJsonVariavel} deve ser do tipo float."
        elif tipo_dado.value == TipoDado.bool.value:
            tipo_dado = self.mapa_tipos.get(TipoDado.bool.value)
            if tipo_dado == type(valor):
                return 200,''
            return 400, f"O valor da propriedade {nomeJsonVariavel} deve ser do tipo booleano."
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
    
    def FindDataProcessingByFilterValue(self,idArquivo,ValorFiltro,tipoOperacao):
        Data = Database()
        response = Data.DoSelect(TratamentoDados,TDOperacao = tipoOperacao,TDIdArquivoProduto = idArquivo,TDValorFiltro = ValorFiltro)
        if len(response) > 0:
            return 400,'Já existe um filtro semelhante a este registrado neste arquivo.'
        return 200,''
    
    def FindDataProcessingByAdditionalFilter(self,idArquivo,ValorConfiguracao,tipoOperacao):
        Data = Database()
        response = Data.DoSelect(TratamentoDados,TDOperacao = tipoOperacao,TDIdArquivoProduto = idArquivo,TDConfiguracoesAdicionais = ValorConfiguracao)
        if len(response) > 0:
            return 400,'Já existe um tratamento de dados semelhante a este registrado neste arquivo.'
        return 200,''
    
    def RemoveDataProcessing(self,idTratamento):
        Data = Database()
        response = Data.DoSelect(TratamentoDados,TDId = idTratamento)
        if len(response) == 0:
            return 400,f'Não foi encontrado o tratamento de dados específico com Id: {idTratamento}'
        response = Data.DoDelete(TratamentoDados,TDId=idTratamento)
        if response is None:
            return 400,'Não foi possível deletar o registro.'
        return 200,''