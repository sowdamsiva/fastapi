from fastapi import  Depends, HTTPException, APIRouter, Request, Form
from sqlmodel import select, Session
from typing import Annotated
from app.models.user_model import CreateUser
# from app.schemas.user_schemas import CreateUser,  Token
from fastapi.security import  OAuth2PasswordRequestForm
# from app.dependencies import SessionDep, get_current_user
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter()

#jinja 2---------------------------------------------------------
from app.database import get_session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

SessionDep = Annotated[Session,Depends(get_session)]

templates = Jinja2Templates(directory="app/templates")

@router.get("/",response_class=HTMLResponse)
def register_form(request:Request):
    return templates.TemplateResponse( request,
        "register.html",
        {
            "request": request
        })

@router.post("/register")
def register_user(session:SessionDep, name:str=Form(...), email:str=Form(...),phone:str=Form(...)):
    users = CreateUser(name=name,email=email,phone=phone)
    session.add(users)
    session.commit()
    return RedirectResponse(url="/users",status_code=303)

@router.get("/users",response_class=HTMLResponse)
def users(session: SessionDep , request:Request):
    users = session.exec(select(CreateUser)).all()
    print("userssssss",users)
    return templates.TemplateResponse( request,"users.html",
        {"request": request,
            "users": users})






# old code--------------------------------------------------------------------

# @router.post("/register")
# def register(session: SessionDep, user_data:CreateUser):
#     if session.exec(select(User).where(User.email==user_data.email)).first():
#         raise HTTPException(status_code=400, detail="Email is already exist")
    
#     hash_pwd = hash_password(user_data.password)
#     user = User(name=user_data.name, email=user_data.email,hashed_password=hash_pwd)
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user

# @router.post("/login", response_model=Token)
# def login(session: SessionDep, form_data : Annotated[OAuth2PasswordRequestForm,Depends()]):
#     user = session.exec(select(User).where(User.email==form_data.username)).first()
#     pwd = verify_password(form_data.password,user.hashed_password)
#     if not user or not pwd:
#         raise HTTPException(status_code=400,detail="Invalid credentials")
    
#     token = create_access_token(data={"sub":user.email})
#     return {"access_token":token, "token_type":"bearer"}


# @router.get("/profile")
# def profile(current_user: Annotated[User,Depends(get_current_user)]):
#     return {"name":current_user.name, "email": current_user.email}
