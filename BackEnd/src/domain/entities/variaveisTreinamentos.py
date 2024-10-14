from data.base import Base
from sqlalchemy import Column, Integer, String, Enum
from src.domain.enum.tipoDado import TipoDado

class VariaveisTreinamentos(Base):
    __tablename__ = 'VariaveisTreinamentos'
    VTId = Column(Integer, primary_key=True, autoincrement=True)
    VTNome = Column(String,nullable=False)
    VTTipoDado = Column(Enum(TipoDado),nullable=False)