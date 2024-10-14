import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum  
from sqlalchemy.orm import relationship
from data.base import Base
from src.domain.enum.tipoOperacao import OperacaoEnum


# Tabela TratamentoDados
class TratamentoDados(Base):
    __tablename__ = 'TratamentoDados'
    TDId = Column(Integer, primary_key=True, autoincrement=True)
    TDConfiguracoesAdicionais = Column(String)    
    TDValorFiltro = Column(String,nullable=False)
    TDOperacao = Column(Enum(OperacaoEnum), nullable=False)
    TDIdArquivoProduto = Column(Integer, ForeignKey('ArquivosProdutos.APId'),nullable=False)
    TDIdUsuario = Column(Integer, ForeignKey('Usuarios.USUid'),nullable=False)

    # Relacionamentos
    ArquivoProdutos = relationship('ArquivoProdutos', back_populates='TratamentoDados')
    Usuarios = relationship('Usuarios', back_populates='TratamentoDados')
    

    
    

