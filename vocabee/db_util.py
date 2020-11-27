from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from vocabee.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
sessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)
Base = declarative_base()
