from app.database import *
from pydantic import BaseModel
from schemas.AnnounceModels import *
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
class Announcement(Base):
    __tablename__ = "announcements"
    announce_id = Column(Integer, primary_key = True, index = True)
    type = Column(String, index = True)
    price = Column(Integer)
    address = Column(String)
    area = Column(Integer)
    rooms_count = Column(Integer)
    description = Column(String)
    user_id = Column(ForeignKey("users.user_id"))

class AnnouncementRepository:
    def save(self, db: Session, announce: PostAnnouncement, user_id):
        announce = Announcement(
            type = announce.type,
            price = announce.price, 
            address = announce.address,
            area = announce.area,
            rooms_count = announce.rooms_count,
            description = announce.description,
            user_id = user_id
            )
        db.add(announce)
        db.commit()
        db.refresh(announce)
        return announce.announce_id
    
    def getAll():
        pass

    def get_by_username():
        pass

    def get_by_id(self, db: Session, announce_id: int):
        announce = db.query(Announcement).filter(Announcement.announce_id == announce_id).first()
        return announce
    
    def update(self, db: Session, announce_id: int, user_id: int,  announce = UpdateAnnouncement):
        
        db.query(Announcement).filter(and_(Announcement.announce_id == announce_id, Announcement.user_id == user_id)).update({
            Announcement.address: announce.address,
            Announcement.area: announce.area,
            Announcement.price: announce.price,
            Announcement.type: announce.type,
            Announcement.rooms_count: announce.rooms_count,
            Announcement.description: announce.description
        })
        db.commit()
        return True
    
    def delete(self, db: Session, announce_id: int, user_id: int):
        announce = db.query(Announcement).filter(and_(Announcement.announce_id == announce_id, Announcement.user_id == user_id)).first()
        if not announce: 
            return False
        db.query(Announcement).filter(Announcement.announce_id == announce_id).delete()
        db.commit()
        return True


   