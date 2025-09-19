from fastapi import FastAPI,Response,status,HTTPException,Depends
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi.responses import JSONResponse
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session



app=FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published : bool=True
    # review: Optional[int]=None
while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='pratik.29',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("database connection was succesfull!")
        break
    except Exception as error:
        print("connection to databse failed ")
        print("error : ",error)
        time.sleep(3)




mypost=[{"title":"this is india","content":"make india proud","id":1},{"title":"this is uttarpredesh","content":"make uttarpradesh  proud","id":2}]

@app.get("/")
async def root():
    return {"message": "hello world "}


@app.get("/getpost")
async def seeAllPost():
    cursor.execute("""select * from posts""")
    post=cursor.fetchall()
    print(post)
    return {"data": post}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    # post_dict=post.dict()
    # post_dict['id']=randrange(0,10000000)
    # mypost.append(post_dict)
    cursor.execute(""" insert into posts (title,content,published) values (%s,%s,%s) returning * """,(post.title,post.content,post.published))

    new_post=cursor.fetchone()
    conn.commit()
    return {"data":new_post}

def findpost(id):
    for p in mypost:
        if p["id"]==id:
            return p
        
def find_post_index(id):
    for i,p in enumerate(mypost):
        if p['id'] == id:
            return i

        


# this rout can not be placed below the post/{id} bcaues in fastapi order maintain from top to bottom 
# this match with path in both so it nick the id one so it will give error
@app.get('/path/latest')
def seeLatest():
    cursor.execute("""select * from posts order by created_at desc limit 1""")
    latestpost=cursor.fetchone();
    return {"the post is ":latestpost}

@app.get("/post/{id}")
def see_specificpost(id:str):
    cursor.execute("""  select * from posts where id= %s """,(id,))
    post=cursor.fetchone()
    
    if not post:
        # return JSONResponse(status_code=404,content={"message":"no such post exist"})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found any post with id {id}")
    return {"the post is":post}


@app.delete("/delete/{id}")
def deletepost(id:int):
    # deleteing post
    # find the index in the areay that has required Id

    cursor.execute("""delete from posts where id=%s returning *  """,(id,))
    deleted_post=cursor.fetchone()
    conn.commit()
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this {id} does not found")
    # return {"message ": "post was sucessfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts{id}")
def update_post(id:int ,post:Post):
    # index=find_post_index(id)
    cursor.execute("""update posts set title=%s,content=%s,published=%s where id=%s returning * """,(post.title,post.content,post.published,id,))
    updated_post=cursor.fetchone()
    conn.commit()


    if updated_post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this  {id} does not exit")
    return {"mesaage": updated_post}



