from app.database import *
from pydantic import BaseModel
from schemas.UsersModel import CreateUser, UpdateUser
from sqlalchemy.orm import Session

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key = True, index = True)
    username = Column(String, index = True)
    phone = Column(String)
    password = Column(String)
    name = Column(String)
    city = Column(String)

class UsersRepository:
    def save(self, db: Session, user: CreateUser):
        db_user = User(username = user.username,  phone = user.phone, password = user.password, name = user.name, city = user.city)
        isHasInDB = db.query(User).filter(User.username == user.username).first()
        if isHasInDB:
            return 0
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user.user_id

    def getAll(self):
        pass

    def get_by_username(self, db: Session, username: str):
        user = db.query(User).filter(User.username == username).first()
        return user

    def get_by_id(self):
        pass

    def update(self, db: Session, username: str, user: UpdateUser):
        db.query(User).filter(User.username == username).update({User.phone: user.phone, User.name: user.name, User.city: user.city})
        db.commit()
        return True


   