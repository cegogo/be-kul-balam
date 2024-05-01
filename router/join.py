from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import GroupMembershipRequest
from db.models import DbUser, DbGroup
from db import db_join
from db.models import group_membership

router = APIRouter(
    prefix='/groups',
    tags=['groups']
)

@router.post("/{id}/join_group")
def join_group_endpoint(id: int, request: GroupMembershipRequest, username: str, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.id == request.user_id).first()
    group = db.query(DbGroup).filter(DbGroup.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not group:
        raise HTTPException(status_code=404, detail=f"Group with the id '{id}' not found")    
    if user in group.members:
        raise HTTPException(status_code=409, detail=f"User already in the group with the id '{id}'")
    
    # Assuming membership_id is None for now, change as needed
    join_group(db, group_id=id, user_id=user.id, membership_id=None, username=username)
    group.members.append(user)  # Assuming group.members is a list
    # Commit changes to the database session
    return {"message": f"User joined the group with the id '{id}'"}

def join_group(db: Session, group_id: int, user_id: int, membership_id: int, username: str):
    db.execute(group_membership.insert().values(group_id=group_id, user_id=user_id, membership_id=membership_id, username=username))
    db.commit()


@router.put("/{id}/leave_group")
def leave_group_endpoint(id: int, request: GroupMembershipRequest, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.id == request.user_id).first()
    group = db.query(DbGroup).filter(DbGroup.id == id).first()
    if not user or not group:
        raise HTTPException(status_code=404, detail="User or group not found")
    if user in group.members:
        group.members.remove(user)
        db.commit()  # Commit changes to the database session
    return {"message": "User left the group"}
