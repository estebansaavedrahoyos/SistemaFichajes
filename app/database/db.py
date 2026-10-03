from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker , Session , DeclarativeBase



load_dotenv()
DATABASE_URL = getenv("DATABASE_URL")
engine = create_engine(url=DATABASE_URL, echo=True , future=True )
LocalSession = sessionmaker(autoflush=False , class_=Session , bind= engine)

class Base(DeclarativeBase):
    pass

def get_db():
    sesion_local = LocalSession()
    try:
        yield sesion_local 
    finally:
        sesion_local.close() 
        

    
            
            
            
        
    


