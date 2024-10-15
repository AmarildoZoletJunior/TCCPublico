from domain.DTOs.arquivosProdutosDTO import ArquivoProdutosDTO
from domain.DTOs.modelosDTO import ModelosDTO
from domain.DTOs.parametrosTreinamentoDTO import ParametrosTreinamentoDTO
from domain.DTOs.tratamentoDadosDTO import TratamentoDadosDTO
from domain.DTOs.usuariosDTO import UsuariosDTO
from domain.DTOs.variaveisTreinamentoDTO import VariaveisTreinamentosDTO
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from src.config import configuration
import urllib

from domain.entities.arquivosProdutos import ArquivoProdutos
from domain.entities.modelos import Modelos
from domain.entities.parametrosTreinamentos import ParametrosTreinamento
from domain.entities.tratamentoDados import TratamentoDados
from domain.entities.usuarios import Usuarios
from domain.entities.variaveisTreinamentos import VariaveisTreinamentos

from data.base import Base

class Database:
    def __init__(self):
        self.engine = self.ConnectDataBase()
        if isinstance(self.engine, str):
            print(self.engine)
        else:
            self.Session = sessionmaker(bind=self.engine)
            self.VerifyBaseTables()

    def VerifyBaseTables(self):
        try:
            Base.metadata.create_all(self.engine, checkfirst=True)
        except Exception as e:
            print(f"Ocorreu um erro ao criar as tabelas do banco, verifique a conexão")
            print(str(e))

    def ConnectDataBase(self):
        try:
            params = urllib.parse.quote_plus(
                f"DRIVER={configuration.DRIVER};"
                f"SERVER={configuration.SERVER};"
                f"DATABASE={configuration.DATABASE};"
                f"Trusted_Connection=yes;"
            )
            engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", echo=False)
            with engine.connect() as connection:
                pass
            return engine
        except Exception as e:
            error_message = f'Ocorreu um erro ao conectar-se ao banco de dados: {str(e)}'
            return error_message
        
        

    def DoSelectWithRelations(self, model, relacoes=None, filtros=None):
        if isinstance(self.engine, str):
            return []

        with self.Session() as session:
            query = session.query(model)
            if filtros:
                query = query.filter_by(**filtros)
            if relacoes:
                for relacao in relacoes:
                    query = query.join(relacao)
            results = query.all()
            dto_list = [self.convert_to_dto(result) for result in results]

            return dto_list


    def DoSelect(self, model, **filters):
        if isinstance(self.engine, str):
            return []
        try:
            with self.Session() as session:
                query = session.query(model).filter_by(**filters)
                results = query.all()
                dto_list = [self.convert_to_dto(result) for result in results]
                return dto_list
        except Exception as e:
            print(f"Erro ao realizar DoSelect: {e}")
            return []

    def objectToDict(self, obj):
        if obj is None:
            return None
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}

    def DoInsert(self, model, **data):
        if isinstance(self.engine, str):
            return None
        with self.Session() as session:
            try:
                new_record = model(**data)
                session.add(new_record)
                session.commit()
                return self.objectToDict(new_record)
            except Exception as e:
                session.rollback()
                print(f"Erro ao inserir dados: {e}")
                return None
            
    def DoUpdate(self, model, filters: dict, update_data: dict):
        if isinstance(self.engine, str):
            return None
        
        with self.Session() as session:
            try:
                query = session.query(model).filter_by(**filters)
                updated_count = query.update(update_data, synchronize_session=False)
                session.commit()
                return updated_count
            except Exception as e:
                session.rollback()
                print(f"Erro ao atualizar dados: {e}")
                return None
            
            
    def DoDelete(self, model, **filters):
        if isinstance(self.engine, str):
            return None
        with self.Session() as session:
            try:
                query = session.query(model).filter_by(**filters)
                deleted_count = query.delete(synchronize_session=False)
                session.commit()
                return deleted_count
            except Exception as e:
                session.rollback()
                print(f"Erro ao deletar dados: {e}")
                return None

    
    def convert_to_dto(self, model_instance):
        if isinstance(model_instance, ArquivoProdutos):
            return ArquivoProdutosDTO(
                model_instance.APId,
                model_instance.APQtdeProdutos,
                model_instance.APDataPostagem,
                model_instance.APArquivo,
                model_instance.APIdUsuario,
                model_instance.APVersao
            ).to_dict()
        
        elif isinstance(model_instance, Modelos):
            return ModelosDTO(
                model_instance.MDId,
                model_instance.MDVersao,
                model_instance.MDArquivo,
                model_instance.MDIdArquivoProd,
                model_instance.MDIdUsuario,
                model_instance.MDDataPostagem,
                usuario=self.convert_to_dto(model_instance.Usuarios) if model_instance.Usuarios else None,
                arquivo_produto=self.convert_to_dto(model_instance.ArquivoProdutos) if model_instance.ArquivoProdutos else None
            ).to_dict()
        
        elif isinstance(model_instance, ParametrosTreinamento):
            return ParametrosTreinamentoDTO(
                model_instance.APId,
                model_instance.APNumPca,
                model_instance.APQtdeRecomendacoes,
                model_instance.APIdArquivoProduto,
                model_instance.APIdUsuario,
                arquivo_produto=self.convert_to_dto(model_instance.ArquivoProdutos) if model_instance.ArquivoProdutos else None,
                usuario=self.convert_to_dto(model_instance.Usuarios) if model_instance.Usuarios else None
            ).to_dict()

        elif isinstance(model_instance, TratamentoDados):
            return TratamentoDadosDTO(
                model_instance.TDId,
                model_instance.TDConfiguracoesAdicionais,
                model_instance.TDValorFiltro,
                model_instance.TDOperacao,
                model_instance.TDIdArquivoProduto,
                model_instance.TDIdUsuario
            ).to_dict()
        
        elif isinstance(model_instance, Usuarios):
            return UsuariosDTO(
                model_instance.USUid,
                model_instance.USUsername,
                model_instance.USUpassword,
            ).to_dict()
        
        elif isinstance(model_instance, VariaveisTreinamentos):
            return VariaveisTreinamentosDTO(
                model_instance.VTId,
                model_instance.VTNome,
                model_instance.VTTipoDado
            ).to_dict()

        return None


            
            
            
