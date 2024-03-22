from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
from database import Base


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return '<User %r?' % (self.name)
    

class Note(Base):
    __tablename__ = 'notes'

    id = Column(String, primary_key=True)
    title = Column(String)
    content = Column(String)
    created = Column(DateTime)
    
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", backref="notes")

    def __repr__(self):
        return '<Note %r>' % (self.title)