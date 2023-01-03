from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.variables import DB_CONNECTION

engine=create_engine(DB_CONNECTION)

Session=sessionmaker(bind=engine)

Base=declarative_base()