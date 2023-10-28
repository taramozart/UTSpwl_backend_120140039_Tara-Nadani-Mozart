from sqlalchemy import Column, Integer, Text
from .meta import Base

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    gambar = Column(Text, nullable=True)
    stok = Column(Integer, nullable=True)
    