from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.db_friendship import create_friendship, delete_friend_request, get_friend_request, get_friendship_by_users
from db.models import DbFriendship
from schemas import FriendshipCreate, Friendship
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from db.database import get_db

router = APIRouter(
    tags=["friendships"]
)

@router.post("/friends", response_model=Friendship)
def send_friend_request(from_user_id: int, to_user_id: int, db: Session = Depends(get_db)):
    """Send a friend request from one user to another."""
    friendship = get_friendship_by_users(db, from_user_id, to_user_id)
    if friendship:
        raise HTTPException(status_code=400, detail="Friendship request already exists")

    friendship_data = FriendshipCreate(user_id=from_user_id, friend_id=to_user_id)
    return create_friendship(db, friendship_data)


@router.put("/friends/{friendship_id}", response_model=Friendship)
def accept_friend_request(friendship_id: int, db: Session = Depends(get_db)):
    """Accept a friend request."""
    friendship = get_friend_request(db, friendship_id)
    if friendship:
        friendship.accepted = True
        db.commit()
        return friendship
    raise HTTPException(status_code=404, detail="Friendship request not found")


@router.put("/friend/{friendship_id}", response_model=Friendship)
def reject_friend_request(friendship_id: int, db: Session = Depends(get_db)):
    """Reject a friend request."""
    friendship = get_friend_request(db, friendship_id)
    if friendship:
        delete_friend_request(db, friendship_id)
        return friendship
    raise HTTPException(status_code=404, detail="Friendship request not found")


@router.delete("/friends/{friendship_id}", response_model=Friendship)
def unfriend(friendship_id: int, db: Session = Depends(get_db)):
    """Remove a friendship."""
    friendship = db.query(DbFriendship).filter(DbFriendship.id == friendship_id).first()
    if friendship:
        db.delete(friendship)
        db.commit()
        return friendship
    else:
        raise HTTPException(status_code=404, detail="Friendship not found")