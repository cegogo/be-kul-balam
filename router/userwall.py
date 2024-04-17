from schemas import PostBase, PostDisplay, PostUpdate, UserBase
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_post, db_user
from auth.oauth2 import get_current_user
from datetime import datetime
import string
import random
import shutil

router = APIRouter(
    tags=['userwall']
)


@router.post("/posts", response_model=PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_post.create_post(db,request)


#Inert image
@router.post('/posts/image') #first image upload then use in the post??
def upload_image(image: UploadFile = File(...)):
    letter= string.ascii_letters
    rand_str = ''.join(random.choice(letter) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.',1))
    path= f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}

# This endpoint is used to retrieve posts # Get all posts from User 
@router.get("/posts/all")
def posts(db: Session = Depends(get_db)):
    posts = db_post.get_all(db)
    return posts

#get spesific post
@router.get('/posts/{id}') #, response_model=PostDisplay)
def get_post(id:int, db:Session = Depends(get_db)): #secure end-point #token: str = Depends(oauth2_scheme)
    return {
        'data': db_post.get_post(db,id)
    }

#Update Post
@router.put('/posts/{id}', response_model=PostDisplay)
def update_post(id: int, request: PostUpdate, db: Session = Depends(get_db), current_user:UserBase = Depends(get_current_user)):
    # Check if the post exists
    post = db_post.get_post(db, id)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    # Update the post content and image_url
    post = db_post.update_post(db, id, request)
    
    return post


#Delete Post
@router.delete('/posts/{id}')
def delete_post(id:int, db:Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return db_post.delete_post(db, id)





