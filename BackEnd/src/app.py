import io


import jwt
import datetime
from functools import wraps
from flask import Flask, request, jsonify
import pandas as pd
from flasgger import Swagger

from repositories.tratamentoDadosRepository import TratamentoDadosRepository
from repositories.usuariosRepository import UserRepository
from repositories.arquivosProdutosRepository import ArquivosProdutosRepository
from repositories.variaveisTreinamentosRepository import VariaveisTreinamentoRepository
from repositories.parametrosTreinamentoRepository import ParametrosTreinamentoRepository
from repositories.usuariosRepository import UserRepository
from repositories.modelosRepository import ModelosRepository



from src.data.database import Database
from src.config import configuration


data = Database()
app = Flask(__name__)
swagger = Swagger(app)

secret = app.config['SECRET_KEY'] = configuration.CHAVE



def tokenNecessario(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
            else:
                return jsonify({'Erro': 'Formato do token inválido!'}), 401
        else:
            return jsonify({'Erro': 'Token é necessário!'}), 401

        try:
            data = jwt.decode(token, secret, algorithms=["HS256"])
            current_user = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'Erro': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'Erro': 'Token inválido!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def criarTokenJWT(user_id):
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm="HS256")
    return token



@app.route("/login",methods=['POST'])
def SignInAccount():
    try:
        data = request.get_json(force=True)
        UserRep = UserRepository(data)
        response, message = UserRep.ValidUser()
        if not response:
            return jsonify({'Erro': message}), 400
        user_list = UserRep.FindUser()

        if user_list and isinstance(user_list, list) and len(user_list) > 0:
            user = user_list[0]
            user_id = user.get('USUid')
            token = criarTokenJWT(user_id)

            return jsonify({
                'Mensagem': 'Usuário encontrado com sucesso',
                'token': token
            }), 200
        else:
            return jsonify({'Erro': 'Usuário não encontrado'}), 400

    except Exception as e:
        return jsonify({'Erro': f'Ocorreu um erro: {e}'}), 500
    
    
    
    
@app.route("/criar/usuario",methods=['POST'])
def RegisterAccount():
    try:
        data = request.get_json(force=True)
        UserRep = UserRepository(data)
        response,message = UserRep.CreateUser()
        if response == 400:
            return jsonify({'Erro': message}), 400
        else:
            return jsonify({'Mensagem': f'Usuário cadastrado com sucesso'}), 200
    except Exception as e:
        return jsonify({'Erro': f'Ocorreu um erro, erro: {e}'}), 500
    
    
@app.route("/atualizar/senha",methods=['PUT'])
def ResetPassword():
    try:
        data = request.get_json(force=True)
        UserRep = UserRepository(data)
        response,message = UserRep.ResetPassword()
        if response == 400:
            return jsonify({'Erro': message}), 400
        else:
            return jsonify({'Mensagem': f'Usuário cadastrado com sucesso'}), 200
    except Exception as e:
        return jsonify({'Erro': f'Ocorreu um erro, erro: {e}'}), 500
        

    
    
    
@app.route('/enviarArquivoProduto',methods=['POST']) #ok
def UploadProductsFile():
    try:
        Arquivo = ArquivosProdutosRepository(request)
        response,message = Arquivo.InsertDataFile()
        if response == 400:
            return jsonify({'Erro': f'Ocorreu um erro: {message}'}), 400
        return jsonify({'Mensagem': f'Arquivo de produtos registrado com sucesso.'}), 200
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
        
@app.route('/removerArquivoProduto/<int:IdArquivo>',methods=['DELETE']) #ok
def DeleteUploadedProductsFile(IdArquivo):
    try:
        Arquivo = ArquivosProdutosRepository('')
        response,message = Arquivo.RemoveFileProducts(IdArquivo)
        if response == 400:
            return jsonify({'Erro': f'Ocorreu um erro: {message}'}), 400
        return jsonify({'Mensagem': f'Registro de arquivo deletado com sucesso.'}), 200
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
        
        
@app.route('/adicionarParametroTreinamento',methods=['POST']) #ok
def CreateTrainingParameters():
    try:
        data = request.get_json(force=True)
        ParametrosRep = ParametrosTreinamentoRepository(data)
        response,message =  ParametrosRep.CreateParametersToData()
        if response == 400:
            return jsonify({'Erro':f'Ocorreu um erro: {message}'}),400
        return jsonify({'Mensagem': f'Parametro registrado com sucesso.'}), 200
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
        
@app.route('/editarParametroTreinamento/<int:IdParametro>',methods=['PUT']) #ok
def EditTrainingParameters(IdParametro):
    try:
        data = request.get_json(force=True)
        ParametrosRep = ParametrosTreinamentoRepository(data)
        response,message =  ParametrosRep.ModifyParametersData(IdParametro)
        if response == 400:
            return jsonify({'Erro':f'Ocorreu um erro: {message}'}),400
        return jsonify({'Mensagem': f'Parametro registrado com sucesso.'}), 200
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
        
@app.route('/removerParametroTreinamento/<int:IdParametro>',methods=['DELETE']) #ok
def DeleteTrainingParameters(IdParametro):
    try:
        ParametrosRep = ParametrosTreinamentoRepository('')
        response,message =  ParametrosRep.DeleteParameters(IdParametro)
        if response == 400:
            return jsonify({'Erro':f'Ocorreu um erro: {message}'}),400
        return jsonify({'Mensagem': f'Parametro registrado com sucesso.'}), 200
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
        
        
        
    
@app.route('/listarTodosModelos',methods=['GET'])
def ListAllTrainingModels():
    try:
        print("")
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
        
@app.route('/gerarModelo',methods=['POST'])
def GenerateModel():
    try:
        data = request.get_json(force=True)
        Modelos = ModelosRepository(data)
        response,message = Modelos.RegisterModelOfTraining()
        return jsonify({'Mensagem': message}), response
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
        
@app.route('/removerModelo/<int:IdModelo>',methods=['DELETE'])
def DeleteModel(IdModelo):
    try:
        print("")
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
        
    
        
        
        
        
        
@app.route('/criarTratamentoDados',methods=['POST']) #ok
def CreateDataProcessing():
    try:
        data = request.get_json(force=True)
        TratamentoDados = TratamentoDadosRepository(data)
        response,message = TratamentoDados.CreateDataProcessing()
        if response == 400:
            return jsonify({'Erro': f'Ocorreu um erro: {message}'}), 400
        return jsonify({'Mensagem': f'Arquivo de produtos registrado com sucesso.'}), 200
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
        
@app.route('/removerTratamentoDados/<int:IdTratamento>',methods=['DELETE']) #ok
def DeleteDataProcessing(IdTratamento):
    try:
        TratamentoDados = TratamentoDadosRepository('')
        response,message = TratamentoDados.RemoveDataProcessing(IdTratamento)
        if response == 400:
             return jsonify({'Erro': f'Ocorreu um erro: {message}'}), 400
        return jsonify({'Mensagem': f'Registro de tratamento de dados removido com sucesso.'}), 200
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
    
    
    
    
    
    
    
    
    
@app.route('/adicionarVariavel',methods=['POST']) #ok
def CreateVariable():
    try:
        data = request.get_json(force=True)
        variavelRep = VariaveisTreinamentoRepository(data)
        response,message = variavelRep.CreateVariable()
        if response == 400:
            return jsonify({'Erro': f'Ocorreu um erro: {message}'}), 400
        return jsonify({'Mensagem': f'Variável registrada com sucesso.'}), 200
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
    
        
@app.route('/editarVariavel/<int:idVariavel>',methods=['PUT']) #ok
def UpdateVariable(idVariavel):
    try:
        data = request.get_json(force=True)
        variavelRep = VariaveisTreinamentoRepository(data)
        response,message = variavelRep.UpdateVariable(idVariavel)
        if response == 400:
            return jsonify({'Erro': f'Ocorreu um erro: {message}'}), 400
        return jsonify({'Mensagem': f'Variável editada com sucesso.'}), 200
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
    
@app.route('/removerVariavel/<int:idVariavel>',methods=['DELETE']) #ok
def DeleteVariable(idVariavel):
    try:
        variavelRep = VariaveisTreinamentoRepository('')
        response,message = variavelRep.DeleteVariable(idVariavel)
        if response == 400:
            return jsonify({'Erro': f'Ocorreu um erro: {message}'}), 400
        return jsonify({'Mensagem': f'Variável removida com sucesso.'}), 200
    except Exception as error:
        return jsonify({'Erro': f'Ocorreu um erro: {error}'}), 500
               
        