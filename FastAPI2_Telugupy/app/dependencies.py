from fastapi import  Depends, HTTPException
from sqlmodel import Session,select
from typing import Annotated
# from app.models.user_model import User
from app.models.user_model import User
from fastapi.security import OAuth2PasswordBearer
from app.database import get_session
from app.auth import verify_token

# SessionDep = Annotated[Session,Depends(get_session)]

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# def get_current_user(token: Annotated[str,Depends(oath2_scheme)], session: SessionDep):
#     payload = verify_token(token)
#     if not payload:
#         raise HTTPException(status_code=401,detail="invalid token")
#     user = session.exec(select(User).where(User.email==payload.get("sub"))).first()
#     if not user:
#         raise HTTPException(status_code=404,detail="user nor found")
#     return user
