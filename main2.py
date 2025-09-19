from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi.responses import JSONResponse

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published : bool=True
    review: Optional[int]=None

mypost=[{"title":"this is india","content":"make india proud","id":1},{"title":"this is uttarpredesh","content":"make uttarpradesh  proud","id":2}]

@app.get("/")
async def root():
    return {"message": "hello world "}

@app.get("/getpost")
async def seeAllPost():
    return {"data":mypost}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,10000000)
    mypost.append(post_dict)
    return {"data":post_dict}

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
    post=mypost[len(mypost)-1]
    return {"the post is ":post}

@app.get("/post/{id}")
def see_specificpost(id:int):
    post=findpost(id)
    if not post:
        # return JSONResponse(status_code=404,content={"message":"no such post exist"})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found any post with id {id}")
    return {"the post is":post}


@app.delete("/delete/{id}")
def deletepost(id:int):
    # deleteing post
    # find the index in the areay that has required Id

    index=find_post_index(id)

    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this {id} does not found")

    mypost.pop(index)
    # return {"message ": "post was sucessfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts{id}")
def update_post(id:int ,post:Post):
    index=find_post_index(id)

    if index ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"psost with this  {id} does not exit")
    
    post_dict =post.dict()
    post_dict['id']=id
    mypost[index]=post_dict
    return {"mesaage": "updated post"}



