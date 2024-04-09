from typing import List
from schemas import UserBase,UserDisplay, UserProductDisplay, Friendship
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_user
from auth.oauth2 import get_current_user
from db.models import DbFriendship


router = APIRouter(
    prefix= '/users',
    tags=['user']
)

#Create User
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)

#Read All Users
@router.get('/all', response_model=List[UserDisplay])
def get_all_users(db: Session= Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user.get_all_user(db)

#Read a user
@router.get('/{id}', response_model=UserDisplay)
def get_user(id: int, db:Session =  Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user.get_user(db, id)

#Update User
@router.put('/{id}', response_model=UserDisplay)
def update_user(id: int, request:UserBase, db:Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user.update_user(db, id, request)

# Delete User
@router.delete('/{id}')
def delete_user(id:int, db:Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_user.delete_user(db, id)

#Get product by user id
@router.get('/{id}/products', response_model=UserProductDisplay)
def get_product_by_user_id (id: int, db: Session = Depends (get_db)):
    return db_user.get_product_by_user_id (db, id)

@router.get("/{id}/friends", response_model=List[Friendship])
def get_friends(id: int, db: Session = Depends(get_db)):
    """Get a list of friendships for a given user."""
    friendships = db.query(DbFriendship).filter(
        (DbFriendship.user_id == id) | (DbFriendship.friend_id == id)
    ).all()
    
    all_friendships = []
    
    for friendship in friendships:
        if friendship.user_id == id:
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

