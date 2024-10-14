from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data.base import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

# Tabela Usuarios
class Usuarios(Base):
    __tablename__ = 'Usuarios'
    USUid = Column(Integer, primary_key=True, autoincrement=True)
    USUsername = Column(String,nullable=False)
    USUpassword = Column(String,nullable=False)
    USUcreated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    
    # Relacionamentos
    Modelos = relationship('Modelos', back_populates='Usuarios')
    ArquivoProdutos = relationship('ArquivoProdutos', back_populates='Usuarios')
    ParametrosTreinamento = relationship('ParametrosTreinamento', back_populates='Usuarios')
    TratamentoDados = relationship('TratamentoDados', back_populates='Usuarios')
