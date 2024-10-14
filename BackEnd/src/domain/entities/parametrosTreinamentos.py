from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from data.base import Base


# Tabela ParametrosTreinamentos
class ParametrosTreinamento(Base):
    __tablename__ = 'ParametrosTreinamento'
    APId = Column(Integer, primary_key=True, autoincrement=True)
    APNumPca = Column(Integer,nullable=False)
    APQtdeRecomendacoes = Column(Integer,nullable=False)
    APIdArquivoProduto = Column(Integer, ForeignKey('ArquivosProdutos.APId'),nullable=False)
    APIdUsuario = Column(Integer, ForeignKey('Usuarios.USUid'),nullable=False)

    # Relacionamentos
    ArquivoProdutos = relationship('ArquivoProdutos', back_populates='ParametrosTreinamento')
    Usuarios = relationship('Usuarios', back_populates='ParametrosTreinamento')