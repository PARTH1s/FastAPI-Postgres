from sqlalchemy import Column, Integer, String
from database import Base

class Table1(Base):
    __tablename__ = "table1"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(String)
