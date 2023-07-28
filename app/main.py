from fastapi import FastAPI, Response, Request, Depends, Form, HTTPException, Cookie
from pydantic import BaseModel
from app.database import SessionLocal, engine
from schemas.UsersModel import CreateUser, UpdateUser
from schemas.AnnounceModels import *
from schemas.CommentModel import *
from app.users_repository import User, UsersRepository
from app.comments_repository import Comment, CommentsRepository
from app.announcement_repository import Announcement, AnnouncementRepository
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
    token: Annotated[str, Depends(oauth2_schema)]):
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
        user_id = decode_jwt(token)['user_id']
        session = SessionLocal()
        isUpdated = announce_repo.update(session, announce_id, user_id, announce)
        if not isUpdated:
            return Response("User hasn't allow to change this announce")
        return Response("Announce successfully has changed")
    finally:
        session.close()

@app.delete("/shanyraks/{announce_id}")
def delete_announcement(
    announce_id : int,
    token: Annotated[str, Depends(oauth2_schema)]):
    try:
        session = SessionLocal()
        user_id = decode_jwt(token)['user_id']
        isDeleted = announce_repo.delete(session, announce_id, user_id)
        if not isDeleted:
            return Response("User hasn't allow to delete this announce")
        return Response("Announce successfully has deleted")
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
        isUpdated = comments_repo.update(session, announce_id, comment_id, user_id, comment)
        if not isUpdated:
            return Response("Not allowed commands")
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
        isUpdated = comments_repo.delete(session, announce_id, comment_id, user_id)
        if isUpdated:
            return Response("Successfully deleted")
    finally:
        session.close()