from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database
from app import oauth2

router = APIRouter(prefix="/follow", tags=["Follow"])

@router.post("/{user_id}", response_model=schemas.FollowResponse)
def follow_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself.")

    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Check if already following
    follow_exists = db.query(models.Follow).filter(
        models.Follow.follower_id == current_user.id,
        models.Follow.following_id == user_id
    ).first()

    if follow_exists:
        raise HTTPException(status_code=400, detail="Already following this user.")

    new_follow = models.Follow(follower_id=current_user.id, following_id=user_id)
    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)
    return new_follow

@router.delete("/{user_id}")
def unfollow_user(
    user_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    follow = db.query(models.Follow).filter(
        models.Follow.follower_id == current_user.id,
        models.Follow.following_id == user_id
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="Not following this user.")

    db.delete(follow)
    db.commit()
    return {"message": "Unfollowed successfully."}

@router.get("/followers/{user_id}", response_model=List[schemas.FollowResponse])
def get_followers(user_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Follow).filter(models.Follow.following_id == user_id).all()

@router.get("/following/{user_id}", response_model=List[schemas.FollowResponse])
def get_following(user_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Follow).filter(models.Follow.follower_id == user_id).all()
