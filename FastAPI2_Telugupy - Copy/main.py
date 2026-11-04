from fastapi import FastAPI, Depends, HTTPException, Form, UploadFile, File
from sqlmodel import SQLModel, create_engine, Session,select
from contextlib import asynccontextmanager
from typing import Annotated
from models import User,CreateUser, LoginUser, Token
import os, shutil
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime,timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

DATABASE_URL= "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, echo=True)

@asynccontextmanager
async def lifespan(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_session)]

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#jwt
SECRET_KET = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None=None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KET, algorithm=ALGORITHM)

def verify_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KET,algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None

def get_current_user(token: Annotated[str,Depends(oath2_scheme)], session: SessionDep):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401,detail="invalid token")
    user = session.exec(select(User).where(User.email==payload.get("sub"))).first()
    if not user:
        raise HTTPException(status_code=404,detail="user nor found")
    return user

#Auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain:str, hashed:str) -> bool:
    return pwd_context.verify(plain, hashed)


@app.post("/register")
def register(session: SessionDep, user_data:CreateUser):
    if session.exec(select(User).where(User.email==user_data.email)).first():
        raise HTTPException(status_code=400, detail="Email is already exist")
    
    hash_pwd = hash_password(user_data.password)
    user = User(name=user_data.name, email=user_data.email,hashed_password=hash_pwd)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/login", response_model=Token)
def login(session: SessionDep, form_data : Annotated[OAuth2PasswordRequestForm,Depends()]):
    user = session.exec(select(User).where(User.email==form_data.username)).first()
    pwd = verify_password(form_data.password,user.hashed_password)
    if not user or not pwd:
        raise HTTPException(status_code=400,detail="Invalid credentials")
    
    token = create_access_token(data={"sub":user.email})
    return {"access_token":token, "token_type":"bearer"}


@app.get("/profile")
def profile(current_user: Annotated[User,Depends(get_current_user)]):
    return {"name":current_user.name, "email": current_user.email}







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