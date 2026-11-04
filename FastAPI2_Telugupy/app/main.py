from fastapi import FastAPI, Depends, HTTPException, Form, UploadFile, File
from sqlmodel import SQLModel, create_engine, Session,select
from contextlib import asynccontextmanager
from typing import Annotated
import os, shutil
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime,timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import create_tables_database
from app.routes import user_routes
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables_database()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(user_routes.router)










# ---------------------------------(2)--------------------------------------
# UPLOAD_DIRS = "upload"
# os.makedirs(UPLOAD_DIRS, exist_ok=True)


# @app.post("/createuser")
# def usercreate(
#     session: SessionDep,
#     name: str = Form(...),
#     phone: str = Form(...),
#     email: str = Form(...),
#     file: UploadFile=File(...)
# ):
#     user_data = {"name":name,"phone":phone,"email":email}
#     validated = CreateUser.model_validate(user_data)

#     file_path = os.path.join(UPLOAD_DIRS,file.filename)
#     with open(file_path,"wb") as f:
#         shutil.copyfileobj(file.file,f)
#     user = User(**validated.model_dump(), file_path=f"{UPLOAD_DIRS}/{file.filename}")

#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user



# ---------------------------------(1)--------------------------------------


# @app.post('/createuser')
# def create_user(user: CreateUser,session: SessionDep):
#     new_user = User.model_validate(user)
#     session.add(new_user)
#     session.commit()
#     session.refresh(new_user)
#     return new_user

# @app.get('/users',response_model=list[User])
# def get_users(session: SessionDep):
#     users = session.exec(select(User)).all()
#     if not users:
#         raise HTTPException(status_code=404,details="user not fund")
#     return users

# @app.get('/user/{user_id}',response_model=User)
# def get_single_user(user_id:int, session:SessionDep):
#     user = session.get(User,user_id)
#     if not user:
#         HTTPException(status_code=404,detail='user not found')
#     return user

# @app.get('/user/{user_id}',response_model=User)
# def update_user(user_id:int, session:SessionDep):
#     user = session.get(User,user_id)
#     if not user:
#         HTTPException(status_code=404,detail='user not found')


# @app.put('/user/{user_id}',response_model=User)
# def update_user(user_id:int,update: CreateUser, session:SessionDep):
#     user = session.get(User,user_id)
#     if not user:
#         HTTPException(status_code=404,detail='user not found')
#     user.name=update.name
#     user.phone = update.phone
#     user.email=update.email
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user

# @app.delete('/user/{user_id}')
# def delete_user(user_id:int, session:SessionDep):
#     user = session.get(User,user_id)
#     if not user:
#         HTTPException(status_code=404,detail='user not found')
#     session.delete(user)
#     session.commit()
#     return {"message":"user deleted successfully"}