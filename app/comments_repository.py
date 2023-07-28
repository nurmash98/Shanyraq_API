from app.database import *
from pydantic import BaseModel
from schemas.CommentModel import AddComment
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import and_, or_
import datetime
class Comment(Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key = True, index = True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    author_id = Column(ForeignKey("users.user_id"))
    announce_id = Column(ForeignKey("announcements.announce_id"))

class CommentsRepository:
    def save(self, db: Session, user_id: int, announce_id: int, comment: AddComment):
        comment = Comment(content = comment.content, author_id = user_id, announce_id = announce_id)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment.comment_id
    def get_by_announceID(self, db: Session, announce_id: int):
        comments = db.query(Comment).filter(Comment.announce_id == announce_id).all()
        return comments
    
    def update(self, db: Session, announce_id: int, comment_id: int, user_id: int, comment: AddComment):
        db.query(Comment).filter(and_(Comment.comment_id == comment_id,  Comment.author_id == user_id)).update({Comment.content: comment.content})
        db.commit()
        return True
    
    def delete(self, db: Session, announce_id, comment_id: int, user_id: int):
        db.query(Comment).filter(and_(Comment.comment_id == comment_id,  Comment.author_id == user_id, Comment.announce_id == announce_id)).delete()
        db.commit()
        return True
    


   