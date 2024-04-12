from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm.session import Session 
from db.models import DbPost, DbPostImage
from fastapi import File, UploadFile
import shutil
import random, string

def upload_post_image(db: Session, post_id: int, image: UploadFile = File(...)):
    post = db.query(DbPost).filter(DbPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id '{post_id}' not found")

    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6)) #Generates 6 random letters for img name
    new = f'_{rand_str}.' #Adds the random letters to the file name
    filename = new.join(image.filename.rsplit('.', 1)) #Splits the prefix and adds name in the #1 index (0,1,2...)
    path = f'images/{filename}' #Folder path

    with open(path, 'wb') as buffer: #Saves the file in the path
        shutil.copyfileobj(image.file, buffer)

    new_image = DbPostImage(
        file_path=path,
        post_id=post_id
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

def get_post_image(db: Session, id: int):
    post_image = db.query(DbPostImage).filter(DbPostImage.id == id).first()
    if not post_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with id '{id}' not found."
        )
    return FileResponse(post_image.file_path)

def delete_post_image(db: Session, id: int):
    post_image = db.query(DbPostImage).filter(DbPostImage.id == id).first()
    if not post_image:
        raise HTTPException(status_code=404, detail=f"Image with id '{id}' not found")
    db.delete(post_image)
    db.commit()
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)