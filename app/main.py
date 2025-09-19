from fastapi import FastAPI,Response,status,HTTPException,Depends
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
from fastapi.responses import JSONResponse
# import psycopg2
from app.utils import hash
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from app import models 
from app.models import Post,User
from app import schemas
from app.database import  engine,get_db
from fastapi.staticfiles import StaticFiles

from app.routers import post,user,auth,vote,message,profile,follow
from app.config import settings

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


print(settings.database_username)

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

# when using direct connection by psycopg2

# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='pratik.29',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("database connection was succesfull!")
#         brea
#     except Exception as error:
#         print("connection to databse failed ")
#         print("error : ",error)
#         time.sleep(3)



@app.get("/")
async def root():
    return {"message": "This is the backend for the social media application "}
# my post=[{"title":"this is india","content":"make india proud","id":1},{"title":"this is uttarpredesh","content":"make uttarpradesh  proud","id":2}]
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(message.router)
# app.include_router(comments.router)
app.include_router(follow.router)

# Serve uploaded profile pics from /media
# app.mount("/media", StaticFiles(directory="uploads/profile_pics"), name="media")

# Include your profile router
app.include_router(profile.router)



