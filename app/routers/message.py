from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database, oauth2
from sqlalchemy import or_, and_

router = APIRouter(tags=["Messages"])

@router.post("/messages", response_model=schemas.MessageOut, status_code=status.HTTP_201_CREATED)
def send_message(message: schemas.MessageCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_message = models.Message(
        sender_id=current_user.id,
        receiver_id=message.receiver_id,
        content=message.content
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

@router.get("/messages", response_model=list[schemas.MessageOut])
def get_messages(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    messages = db.query(models.Message).filter(
        (models.Message.sender_id == current_user.id) | 
        (models.Message.receiver_id == current_user.id)
    ).all()
    return messages



@router.get("/messages/conversation/{other_user_id}", response_model=list[schemas.MessageOut])
def get_conversation(other_user_id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    messages = db.query(models.Message).filter(
        or_(
            and_(models.Message.sender_id == current_user.id, models.Message.receiver_id == other_user_id),
            and_(models.Message.sender_id == other_user_id, models.Message.receiver_id == current_user.id)
        )
    ).order_by(models.Message.created_at).all()

    return messages


@router.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    message_query = db.query(models.Message).filter(models.Message.id == message_id)
    message=message_query.first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this message")
    
    # Soft delete
    message_query.delete(synchronize_session=False)
    message.deleted = True
    db.commit()
    return {"message": "Message deleted successfully"}


@router.put("/messages/{message_id}")
def edit_message(message_id: int, update: schemas.MessageUpdate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if message.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this message")
    
    message.content = update.content
    message.edited = True
    db.commit()
    db.refresh(message)
    return message
