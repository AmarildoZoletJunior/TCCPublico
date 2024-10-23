from sqlalchemy import Column, Integer, String, Date, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from data.base import Base

# Tabela ArquivoProdutos
class ArquivoProdutos(Base):
    __tablename__ = 'ArquivosProdutos'
    APId = Column(Integer, primary_key=True, autoincrement=True)
    APQtdeProdutos = Column(Integer)
    APDataPostagem = Column(Date)
    APArquivo = Column(LargeBinary,nullable=False)
    APArquivoDelimiter = Column(String,nullable=False)
    APIdUsuario = Column(Integer, ForeignKey('Usuarios.USUid'),nullable=False)
    APVersao = Column(String,nullable=False)

    # Relacionamentos
    Usuarios = relationship('Usuarios', back_populates='ArquivoProdutos')
    Modelos = relationship('Modelos', back_populates='ArquivoProdutos')
    ParametrosTreinamento = relationship('ParametrosTreinamento', back_populates='ArquivoProdutos')
    TratamentoDados = relationship('TratamentoDados', back_populates='ArquivoProdutos')