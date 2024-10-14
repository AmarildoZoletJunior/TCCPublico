from sqlalchemy import Column, Integer, String, Date, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from data.base import Base

# Tabela Modelos
class Modelos(Base):
    __tablename__ = 'Modelos'
    MDId = Column(Integer, primary_key=True, autoincrement=True)
    MDVersao = Column(String,nullable=False)
    MDArquivo = Column(LargeBinary,nullable=False)
    MDIdArquivoProd = Column(Integer, ForeignKey('ArquivosProdutos.APId'),nullable=False)
    MDIdUsuario = Column(Integer, ForeignKey('Usuarios.USUid'),nullable=False)
    MDDataPostagem = Column(Date)

    # Relacionamentos
    Usuarios = relationship('Usuarios', back_populates='Modelos')
    ArquivoProdutos = relationship('ArquivoProdutos', back_populates='Modelos')