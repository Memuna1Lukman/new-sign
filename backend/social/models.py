from sqlalchemy import Column,Integer,String,TIMESTAMP,text
from .database import Base


class User(Base):
    __tablename__ = "socialUsers"

    
    id= Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    username = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=True)
    google_id = Column(String,nullable=True,unique=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))