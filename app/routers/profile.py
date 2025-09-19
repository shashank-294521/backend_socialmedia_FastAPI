import os
import base64
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app import models, schemas, database, oauth2

router = APIRouter(tags=["Profiles"])

UPLOAD_DIR = "media/profiles"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def encode_image_to_base64(filepath: str) -> str:
    with open(filepath, "rb") as f:
        return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"

@router.post("/profile", response_model=schemas.ProfileOut)
async def create_or_update_profile(
    bio: str = Form(None),
    profile_picture: UploadFile = File(None),
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()

    filename = None
    if profile_picture:
        ext = profile_picture.filename.split(".")[-1].lower()
        if ext not in ["png", "jpg", "jpeg"]:
            raise HTTPException(status_code=400, detail="Only PNG, JPG, JPEG allowed")

        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(await profile_picture.read())

    if profile:
        profile.bio = bio or profile.bio
        if filename:
            profile.profile_picture = filename
    else:
        profile = models.Profile(
            user_id=current_user.id,
            bio=bio,
            profile_picture=filename
        )
        db.add(profile)

    db.commit()
    db.refresh(profile)

    file_path = os.path.join(UPLOAD_DIR, profile.profile_picture) if profile.profile_picture else None
    preview = encode_image_to_base64(file_path) if file_path and os.path.exists(file_path) else None

    return schemas.ProfileOut(
        id=profile.id,
        user_id=profile.user_id,
        bio=profile.bio,
        created_at=profile.created_at,
        profile_picture_url=f"/profile/{profile.user_id}/photo" if profile.profile_picture else None,
        profile_picture_preview=preview
    )

@router.get("/profile/{user_id}", response_model=schemas.ProfileOut)
def get_profile(user_id: int, db: Session = Depends(database.get_db)):
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    file_path = os.path.join(UPLOAD_DIR, profile.profile_picture) if profile.profile_picture else None
    preview = encode_image_to_base64(file_path) if file_path and os.path.exists(file_path) else None

    return schemas.ProfileOut(
        id=profile.id,
        user_id=profile.user_id,
        bio=profile.bio,
        created_at=profile.created_at,
        profile_picture_url=f"/profile/{profile.user_id}/photo" if profile.profile_picture else None,
        profile_picture_preview=preview
    )

@router.get("/profile/{user_id}/photo")
def get_profile_photo(user_id: int, db: Session = Depends(database.get_db)):
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not profile or not profile.profile_picture:
        raise HTTPException(status_code=404, detail="Profile photo not found")

    file_path = os.path.join(UPLOAD_DIR, profile.profile_picture)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)
