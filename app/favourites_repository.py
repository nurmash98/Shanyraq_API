from app.database import *
from pydantic import BaseModel
from sqlalchemy.orm import Session

class Favour(Base):
    __tablename__ = "favours"
    favour_id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable = False)
    announce_id = Column(Integer, ForeignKey("announcements.announce_id"), nullable = False)


class FavoursRepository:
    def save(self, session: Session, user_id: int, announce_id: int):
        new_favour = Favour(user_id = user_id, announce_id = announce_id)
        session.add(new_favour)
        session.commit()
        session.refresh(new_favour)
        return True
    def get_by_user_id(self, session: Session, user_id: int):
        return session.query(Favour).filter(Favour.user_id == user_id).all()
    
    def get_by_id(self, session: Session, favour_id: int):
        return session.query(Favour).filter(Favour.favour_id == favour_id).first()
    
    def delete(self, session: Session, favour_id: int):
        session.query(Favour).filter(Favour.favour_id == favour_id).delete()
        session.commit()
        return True
