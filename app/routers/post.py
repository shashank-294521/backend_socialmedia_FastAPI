from app import models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Optional,List
from app import oauth2,schemas
from sqlalchemy import func

router=APIRouter(
    tags=["Posts"]
)

# @router.get("/getpost",response_model=List[schemas.Post])
@router.get("/getpost",response_model=List[schemas.PostOut])
async def seeAllPost(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    # cursor.execute("""select * from posts""")
    # post=cursor.fetchall()
    # print(post)'

    # print(limit)
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # if u want to see login user ppost only but make user to comment the aabove single line
    # posts=db.query(models.Post).filter(models.Post.user_id==current_user.id).all()

    results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # return  results
    return [{"post": post, "votes": votes} for post, votes in results]

@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    # new_post=models.Post(title=post.title,content=post.content,published=post.published)

    # we have to do this for every coloum let say we have 50 coloumns then for each colounmn
    # u have to do like this title=post.title....... so what we can do is 
    print(current_user.id)
    print(current_user.email)
    new_post=models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post) # add in database
    db.commit()  # commit all the changes 
    db.refresh(new_post)  #returnnig the data as we are doing in postgres returning *
    return new_post

# def findpost(id):
#     for p in mypost:
#         if p["id"]==id:
#             return p
        
# def find_post_index(id):
#     for i,p in enumerate(mypost):
#         if p['id'] == id:
#             return i

        


# this rout can not be placed below the post/{id} bcaues in fastapi order maintain from top to bottom 
# this match with path in both so it nick the id one so it will give error

# @router.get("/post/{id}",response_model=List[schemas.PostOut])
# def see_specificpost(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
#     # post=db.query(models.Post).filter(models.Post.id==id).first()
#     post=results=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).first()
    
#     if not post:
#         # return JSONResponse(status_code=404,content={"message":"no such post exist"})
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"not found any post with id {id}")
    
#     # if making post private
#     # if post.user_id !=current_user.id:
#     #      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authrised to perform the requried action ")
#     # return post
#     return [{"post": post, "votes": votes} for post, votes in results]

@router.get("/post/{id}", response_model=schemas.PostOut)
def see_specificpost(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.id == id)   # <-- filter by id
        .group_by(models.Post.id)
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    post, votes = result
    return {"post": post, "votes": votes}


@router.delete("/delete/{id}")
def deletepost(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # deleteing post
    # find the index in the areay that has required Id
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this {id} does not found")
    # return {"message ": "post was sucessfully deleted"}

    if post.user_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authrised to perform the requried action ")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts{id}",response_model=schemas.Post)
def update_post(id:int ,updated_post:schemas.PostBase,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # # index=find_post_index(id)
    # cursor.execute("""update posts set title=%s,content=%s,published=%s where id=%s returning * """,(post.title,post.content,post.published,id,))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this  {id} does not exit")
    
    if post.user_id !=current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not authrised to perform the requried action ")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return  post_query.first()
