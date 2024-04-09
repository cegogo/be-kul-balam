from fastapi import APIRouter, Depends, HTTPException, Response
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

@router.get("/friendships/{user_id}", response_model=List[Friendship])
def get_friends(user_id: int, db: Session = Depends(get_db)):
    """Get a list of friendships for a given user."""
    friendships = db.query(DbFriendship).filter(
        (DbFriendship.user_id == user_id) | (DbFriendship.friend_id == user_id)
    ).all()
    
    all_friendships = []
    
    for friendship in friendships:
        if friendship.user_id == user_id:
            all_friendships.append({
                "user_id": friendship.user_id,
                "friend_id": friendship.friend_id,
                "id": friendship.id
            })
        else:
            all_friendships.append({
                "user_id": friendship.friend_id,
                "friend_id": friendship.user_id,
                "id": friendship.id
            })
    
    return all_friendships

@router.post("/friendships", response_model=Friendship)
def send_friend_request(from_user_id: int, to_user_id: int, db: Session = Depends(get_db)):
    """Send a friend request from one user to another."""
    friendship = get_friendship_by_users(db, from_user_id, to_user_id)
    if friendship:
        raise HTTPException(status_code=400, detail="Friendship request already exists")

    friendship_data = FriendshipCreate(user_id=from_user_id, friend_id=to_user_id)
    return create_friendship(db, friendship_data)


@router.put("/friendships/{friendship_id}", response_model=Friendship)
def update_friendship_status(friendship_id: int, status: str, db: Session = Depends(get_db)):
    """Update the status of a friendship request."""
    friendship = get_friend_request(db, friendship_id)
    if friendship:
        if status.lower() == "accept":
            friendship.accepted = True
            db.commit()
            return friendship
        elif status.lower() == "reject":
            delete_friend_request(db, friendship_id)
            return friendship
        else:
            raise HTTPException(status_code=400, detail="Invalid status. Use 'accept' or 'reject'.")
    raise HTTPException(status_code=404, detail="Friendship request not found")


@router.delete("/friends/{friendship_id}")
def unfriend(friendship_id: int, db: Session = Depends(get_db)):
    """Remove a friendship."""
    friendship = db.query(DbFriendship).filter(DbFriendship.id == friendship_id).first()
    if friendship:
        db.delete(friendship)
        db.commit()
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Friendship not found")