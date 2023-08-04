from fastapi import FastAPI, Response, Request, Depends, Form, HTTPException, Cookie
from pydantic import BaseModel
from app.database import SessionLocal, engine
from schemas.UsersModel import CreateUser, UpdateUser
from schemas.AnnounceModels import *
from schemas.CommentModel import *
from app.users_repository import User, UsersRepository
from app.comments_repository import Comment, CommentsRepository
from app.announcement_repository import Announcement, AnnouncementRepository
from app.favourites_repository import FavoursRepository
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from typing import List, Annotated
app = FastAPI()
oauth2_schema = OAuth2PasswordBearer(tokenUrl = "/auth/users/login")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

users_repo = UsersRepository()
comments_repo = CommentsRepository()
announce_repo = AnnouncementRepository()
favours_repo = FavoursRepository()
def encode_jwt(username: str, user_id: int) -> str:
    body = {"username" : username, "user_id" : user_id}
    token = jwt.encode(body, "Haha", "HS256")
    return token

def decode_jwt(token: str) -> str:
    data = jwt.decode(token, "Haha", "HS256")
    return data

@app.post("/auth/users")
def post_create_user(user: CreateUser):
    try:
        session = SessionLocal()
        user_id = users_repo.save(session, user)
        if user_id == 0:
            return Response("Such username is already taken")
        return user_id
    finally:
        session.close()

@app.post("/auth/users/login")
def post_login(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        session = SessionLocal()
        username = data.username
        password = data.password
        user = users_repo.get_by_username(session, username)
        if not user:
            raise HTTPException(status_code = 400, detail = "Username not found or password is incorrect")
        if password != user.password:
            raise HTTPException(status_code = 400, detail = "Username not found or password is incorrect")
          
        token = encode_jwt(username, user.user_id)
        return {"access_token": token}
    finally:
        session.close()

@app.patch("/auth/users/me")
def update_profile(
    user: UpdateUser, 
    token: Annotated[str, Depends(oauth2_schema)]) -> Response:
    try:
        session = SessionLocal()
        username = decode_jwt(token)['username']
        isOk = users_repo.update(session, username, user)
        if isOk:
            return Response("Information has changed")
        else:
            return Response("Database error")
    finally:
        session.close()

@app.get("/auth/users/me")
def get_profile(token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        username = decode_jwt(token)['username']
        user = users_repo.get_by_username(session, username)
        return {
            "user_id" : user.user_id,
            "username" : user.username, 
            "phone" : user.phone, 
            "name" : user.name,
            "city" : user.city
        }
    finally:
        session.close()
    
@app.post("/shanyraks")
def post_announcement(
    announce: PostAnnouncement, 
    token: Annotated[str, Depends(oauth2_schema)]) -> int:
    try:
        session = SessionLocal()
        user_id = decode_jwt(token)['user_id']
        announce_id = announce_repo.save(session, announce, user_id)
        return announce_id
    finally:
        session.close()

@app.get("/shanyraks/{announce_id}")
def get_announcement(announce_id : int):
    try:
        session = SessionLocal()
        announce = announce_repo.get_by_id(session, announce_id)
        if not announce:
            raise HTTPException(status_code = 404, detail = "Announce not found")
        return announce
    finally:
        session.close()

@app.patch("/shanyraks/{announce_id}")
def update_announcement(
    announce_id : int,
    announce: UpdateAnnouncement, 
    token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        user_id = decode_jwt(token)['user_id']
        announce = announce_repo.get_by_id(session, announce_id)
        if not announce:
            raise HTTPException(status_code = 404, detail = "Announce not found")
        if announce.user_id != user_id:
            raise HTTPException(status_code=403, detail = "Forbidden")
        announce_repo.update(session, announce_id, user_id, announce)
    finally:
        session.close()

@app.delete("/shanyraks/{announce_id}")
def delete_announcement(
    announce_id : int,
    token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        user_id = decode_jwt(token)['user_id']
        announce = announce_repo.get_by_id(session, announce_id)
        if not announce:
            raise HTTPException(status_code = 404, detail = "Announce not found")
        if announce.user_id != user_id:
            raise HTTPException(status_code=403, detail = "Forbidden")
        announce_repo.delete(session, announce_id, user_id)
    finally:
        session.close()
        
@app.post("/shanyraks/{announce_id}/comments")
def post_comment(
    announce_id: int, 
    comment: AddComment,
    token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        user_id = decode_jwt(token)['user_id']
        comment_id = comments_repo.save(session, user_id, announce_id,comment)
        return comment_id
    finally:
        session.close()

@app.get("/shanyraks/{announce_id}/comments")
def get_comments(announce_id: int):
    try:
        session = SessionLocal()
        comments = comments_repo.get_by_announceID(session, announce_id)
        if not comments:
            raise HTTPException(status_code = 404, detail = "Comments not found")
        return comments
    finally:
        session.close()

@app.patch("/shanyraks/{announce_id}/comments/{comment_id}")
def update_comment(
    announce_id: int, 
    comment_id: int, 
    comment: AddComment,
    token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        user_id = decode_jwt(token)['user_id']
        comment = comments_repo.get_by_id(session, comment_id)
        if not comment:
            raise HTTPException(status_code = 404, detail = "Comment not found")
        if comment.user_id != user_id:
            raise HTTPException(status_code=403, detail = "Forbidden")
        if comment.announce_id!= announce_id:
            raise HTTPException(status_code=403, detail = "Forbidden")
        comments_repo.update(session, comment_id, user_id, comment)
        return Response("Successfully updated")
    finally:
        session.close()

@app.delete("/shanyraks/{announce_id}/comments/{comment_id}")
def delete_comment(
    announce_id: int, 
    comment_id: int,
    token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        user_id = decode_jwt(token)['user_id']
        comment = comments_repo.get_by_id(session, comment_id)
        if not comment:
            raise HTTPException(status_code = 404, detail = "Comment not found")
        if comment.user_id != user_id:
            raise HTTPException(status_code=403, detail = "Forbidden")
        if comment.announce_id!= announce_id:
            raise HTTPException(status_code=403, detail = "Forbidden")
        comments_repo.update(session, comment_id, user_id, comment)
        comments_repo.delete(session, announce_id, comment_id, user_id)
        return Response("Successfully deleted")
        
    finally:
        session.close()

#POST /auth/users/favorites/shanyraks/{id}
@app.post("/auth/users/favorites/shanyraks/{announce_id}")
def post_favorite(
    announce_id: int, 
    token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        user_id = decode_jwt(token)['user_id']
        favorite = favours_repo.save(session, user_id, announce_id)
        return favorite
    finally:
        session.close()

@app.get("/auth/users/favorites/shanyraks")
def get_favorites(token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        user_id = decode_jwt(token)['user_id']
        favorites = favours_repo.get_by_user_id(session, user_id)
        if not favorites:
            raise HTTPException(status_code = 404, detail = "Favorites not found")
        favours = []
        for favour in favorites:
            announce = announce_repo.get_by_id(session, favour.announce_id)
            if not announce:
                raise HTTPException(status_code = 404, detail = "Announce not found")
            favours.append({"id": announce.announce_id, "address": announce.address})
        return {"shanyraks" : favours}
    finally:
        session.close()

@app.delete("/auth/users/favorites/shanyraks/{favour_id}")
def delete_favorite(
    favour_id: int, 
    token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        user_id = decode_jwt(token)['user_id']
        favorite = favours_repo.get_by_id(session, favour_id)
        if not favorite:
            raise HTTPException(status_code = 404, detail = "Favorite not found")
        if favorite.user_id!= user_id:
            raise HTTPException(status_code=403, detail = "Forbidden")
        favours_repo.delete(session, favour_id)
        return Response("Successfully deleted")
    finally:
        session.close()

        
@app.get("/shanyraks")
def get_announcements(query: QueryAnnouncement):
    try:
        session = SessionLocal()
        limit = query.limit
        offset = query.offset
        announcements = announce_repo.get_by_query(session, query)
        if not announcements:
            raise HTTPException(status_code = 404, detail = "Announcements not found")
        if not limit or not offset:
            return announcements
        else:
            start_index = (offset - 1)*limit
            end_index = offset*limit
            return announcements[start_index:end_index]
    finally:
        session.close()
