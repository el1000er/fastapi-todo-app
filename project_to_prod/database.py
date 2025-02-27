from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

## SQL lite connection
SQLACHEMY_DATABASE_URL =  'sqlite:///./project_to_prod/todosapp.db'
engine = create_engine(SQLACHEMY_DATABASE_URL,connect_args={'check_same_thread':False})

# SQLACHEMY_DATABASE_URL =  'postgresql://postgres:asdzxc3033@localhost/TodoApplicationDatabase'
# engine = create_engine(SQLACHEMY_DATABASE_URL )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

