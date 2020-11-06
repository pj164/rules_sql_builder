from uuid import uuid4
from sqlalchemy import Column, Integer, String, Text, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

def generate_uuid():
    return str(uuid4())

class Control_1(Base):
    __tablename__ = 'control_1'
    id = Column("id", String(75), primary_key=True, default=generate_uuid)
    client_id = Column('client_id', Integer, nullable=False)
    user_id = Column('user_id', Integer, nullable=False)
    email = Column('email', String(256), nullable=False)