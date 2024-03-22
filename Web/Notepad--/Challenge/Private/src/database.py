from datetime import datetime
import os
from uuid import uuid1

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine('sqlite:///:memory:', echo=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from models import User, Note
    Base.metadata.create_all(bind=engine)
    
    
    admin = User(username="admin", password="icapxbxtgRF4umPqr5S4")
    superadmin = User(username="superadmin", password="TbVDFG8P3sieEqyofLyS")
    note = Note(id=str(uuid1(node=171701900198059, clock_seq=2)), title="TOP SECRET - Credentials.", content=os.environ["FLAG"], created=datetime.now(), author=superadmin)
    print(f"Generated note with ID: {note.id}")
    db_session.add_all([admin, superadmin, note])
    db_session.commit()
