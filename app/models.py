from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, nullable=False)
    path_image = Column(String, nullable=False)
    prompt = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
    