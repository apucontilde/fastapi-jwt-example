from typing import List
from fastapi import Depends, FastAPI, HTTPException, Body, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from auth import JWTBearer, check_password, create_jwt, hash_password
from db import get_session, engine
from models import UserModel, Base
from schemas import UserSchema, UserCreate, UserInDB, UserLogin, UserSession

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/user/register/", response_model=UserSession)
async def user_register(
    *, session: Session = Depends(get_session), user: UserCreate = Body(...)
):
    user_create: UserInDB = UserCreate.model_validate(user)
    db_user = UserModel(
        email=user_create.email,
        name=user_create.name,
        **hash_password(user_create.password)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    user_session = UserSession(
        access_token=create_jwt(user_id=db_user.id), user_id=db_user.id
    )
    return user_session


@app.post("/login/", response_model=UserSession)
async def login(*, session: Session = Depends(get_session), user: UserLogin):
    db_user = session.execute(
        select(UserModel.id, UserModel.email, UserModel.hashed_password).filter_by(
            email=user.email
        )
    ).first()
    if db_user:
        if check_password(user.password, db_user.hashed_password):
            return create_jwt(db_user.id)
        else:
            raise HTTPException(status_code=401, detail="Uunauthorized")
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.get(
    "/user/",
    dependencies=[Depends(JWTBearer())],
    tags=["user"],
    response_model=List[UserSchema],
)
async def get_users(
    *, session: Session = Depends(get_session), user_id: str | None = None
):
    if user_id:
        db_user: UserModel = session.execute(
            select(UserModel.id, UserModel.email, UserModel.name).filter_by(id=user_id)
        ).first()
        return [UserSchema.model_validate(db_user)]
    else:
        db_users: List[UserModel] = session.execute(
            select(UserModel.id, UserModel.email, UserModel.name)
        ).all()
        return [UserSchema.model_validate(user) for user in db_users]


# main.py

import uvicorn

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8081, reload=True)
