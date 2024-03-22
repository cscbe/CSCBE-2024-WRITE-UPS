from sqlalchemy import schema, create_engine, Column, Integer, String, ForeignKey, BLOB, StaticPool
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, Relationship, declarative_base
from sqlalchemy.ext.compiler import compiles
from argon2 import argon2_hash
from os import urandom, makedirs
import random
import string
from uuid import uuid4
from dataclasses import dataclass
from pathlib import Path
import shutil

# GOOD LUCK STEALING MY DATABASE WHEN IT'S ALL IN MY HEAD!
engine = create_engine('sqlite:///:memory:', connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=False)
db_session = scoped_session(sessionmaker(autoflush=True, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

@compiles(schema.CreateTable)
def compile(element, compiler, **kw) -> str:
    text = compiler.visit_create_table(element, **kw)
    if element.element.info.get('without_rowid'):
        text = text.rstrip() + ' WITHOUT ROWID\n\n'
    return text

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'info': {'without_rowid': True}}

    id = Column(String, primary_key=True)
    username = Column(String)
    password = Column(BLOB)
    salt = Column(BLOB)
    guest_of: Relationship["RepositoryGuest"] = relationship("RepositoryGuest", back_populates="guest")
    owner_of = relationship("Repository", back_populates="owner")

    def __repr__(self):
        return f"User Object: {self.username} with ID {self.id}"
    
    def compare_passwords(self, password: str):
        # HA, NO INSECURE PASSWORD STORAGE FOR YOU
        return argon2_hash(password, self.salt) == self.password
    
    def update_password(self, new_password: str):
        # HA, NO INSECURE PASSWORD STORAGE FOR YOU
        self.password = argon2_hash(new_password, self.salt)
        db_session.commit()
    
    def delete(self):
        # HA, NO UNTRACKED REPOSITORIES FOR YOU
        repositories = db_session.query(Repository).filter(Repository.owner_id == self.id).all()
        for repository in repositories:
            repository.delete()
        guest_tickets = db_session.query(RepositoryGuest).filter(RepositoryGuest.guest_id == self.id).all()
        for ticket in guest_tickets:
            db_session.delete(ticket)
        db_session.delete(self)
        db_session.commit()
    
    @staticmethod
    def from_id(id: str):
        return db_session.query(User).filter(User.id==id).first()
    
    @staticmethod
    def from_username(username: str):
        return db_session.query(User).filter(User.username==username).first()
    
    @staticmethod
    def admin() -> "User":
        adminuser = User.from_username("admin")
        if not adminuser:
            raise NameError("Failed to find the admin user")
        return adminuser
    
    @staticmethod
    def new(username: str, password: str):
        # HA, NO PASSWORD CRACKING FOR YOU
        # THIS SALT, IT COMES
        #      FROM
        #      YOUR
        #     TEARS!
        # KEEP CRYING BABY :3 YOU'LL NEVER GET ME!
        salt = urandom(32)
        user = User(
            # HA, NO UUID GUESSING FOR YOU
            id=str(uuid4()),
            username=username,
            # HA, NO INSECURE PASSWORD STORAGE FOR YOU
            password=argon2_hash(password, salt),
            salt=salt,
        )
        db_session.add(user)
        db_session.commit()
        return user

class Repository(Base):
    __tablename__ = "repository"
    __table_args__ = {'info': {'without_rowid': True}}
    
    id = Column(String, primary_key=True)
    name = Column(String)
    owner_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="owner_of")
    guests = relationship("RepositoryGuest", back_populates="repository")

    @property
    def folder(self):
        return Path(f"./repository/{self.id}")  
    
    def is_at_least_guest(self, current_user: User):
        return str(self.id) != "global" and (current_user.id not in [guest.guest_id for guest in self.guests] and current_user.id != self.owner.id)
    
    def is_at_least_owner(self, current_user: User):
        return current_user.id != self.owner.id

    def share_with(self, target_user: User):
        guest_ticket = RepositoryGuest(guest=target_user, repository=self)
        db_session.add(guest_ticket)
        db_session.commit()
    
    def unshare_with(self, target_user: User):
        guest_ticket = db_session.query(RepositoryGuest).filter(RepositoryGuest.guest_id == target_user.id, RepositoryGuest.repository_id == self.id).first()
        db_session.delete(guest_ticket)
        db_session.commit()
    
    def delete(self):
        folder = self.folder
        guest_tickets = db_session.query(RepositoryGuest).filter(RepositoryGuest.repository_id == self.id).all()
        # HA, NO UNTRACKED REFERENCES FOR YOU
        for ticket in guest_tickets:
            db_session.delete(ticket)
        db_session.delete(self)
        db_session.commit()
        shutil.rmtree(folder, ignore_errors=True)

    @staticmethod
    def from_id(id: str):
        return db_session.query(Repository).filter(Repository.id==id).first()
    
    @staticmethod
    def get_all_for(user: User):
        if not user:
            return {"owned":[],"shared_with":[], "global":db_session.query(Repository).get("global")}
        
        return {
            "owned": db_session.query(Repository).filter(Repository.owner_id == user.id).all(),
            "shared_with": db_session.query(Repository).filter(Repository.guests.any(RepositoryGuest.guest_id == user.id)).all(),
            "global":db_session.query(Repository).get("global"),
        }
    
    @staticmethod
    def new(owner: User, name: "str|None" = None):
        # HA, NO UUID GUESSING FOR YOU
        repo_id=str(uuid4())
        repository = Repository(
            id=repo_id,
            name=name or repo_id,
            owner=owner,
        )
        makedirs(f"./repository/{repository.id}")
        admin_guest_ticket = RepositoryGuest(guest=User.admin(), repository=repository)
        db_session.add_all([repository, admin_guest_ticket])
        db_session.commit()
        return repository

class RepositoryGuest(Base):
    __tablename__ = "repositoryguest"
    
    relation_id = Column(Integer, primary_key=True)
    guest_id = Column(String, ForeignKey("users.id"))
    repository_id = Column(String, ForeignKey("repository.id"))
    guest = relationship("User", back_populates="guest_of")
    repository = relationship("Repository", back_populates="guests")

@dataclass
class PackageManifest:
    name: str
    version: str
    author: str
    publisher: str
    actions: "list[dict]"
    
    @staticmethod
    def from_yaml(yaml_object: dict):
        return PackageManifest(
            name=yaml_object['name'],
            author=yaml_object['author'],
            version=yaml_object['version'],
            publisher=yaml_object['publisher'],
            actions=yaml_object['actions'],
        )
    
def init_db():
    Base.metadata.create_all(bind=engine)
    
    
    # GOOD LUCK CRACKING THIS HAHAHAHAHAHAHAAAHAHAHAHAH
    admin_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    admin_salt = urandom(32)
    # HA, NO UUID GUESSING *OR* PASSWORD CRACKING FOR YOU :D
    admin = User(id=str(uuid4()), username="admin", password=argon2_hash(admin_pass, admin_salt), salt=admin_salt)
    global_repository = Repository(id="global", name="Global Package Repository", owner=admin)
    
    db_session.add_all([admin, global_repository])
    db_session.commit()
    print(f"Generated admin with password {admin_pass}")