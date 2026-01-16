from operator import mul
import string
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.src.db import db_article
from backend.src.schemas.article_schema import ArticleBase, ArticleDisplay, ArticleEditDisplay, VoteBase
from backend.src.db.database import get_db
from backend.src.schemas.user_schema import UserBase
from backend.src.utils.auth_service.oauth2_util import get_current_user
import random
import shutil

router = APIRouter()

@router.post("/")
def blogs_root():
    """
    Root endpoint for blogs post.
    """
    return {"message": "Welcome to the blogs post root!"}

@router.post("/create",response_model=ArticleDisplay)
def create_article(request: ArticleBase, db:Session= Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    """
    Endpoint to create a new blog post.
    """
    request.author_id = current_user.id
    return db_article.create_article(db,request=request)

@router.post("/edit",response_model=ArticleDisplay)
def edit_article(request: ArticleEditDisplay, db:Session= Depends(get_db),current_user: UserBase = Depends(get_current_user)):
    """
    Endpoint to edit an existing blog post.
    """
    return db_article.edit_article(db,request=request, current_user=current_user.id)

@router.post('/vote',response_model=VoteBase)
def vote_article(request: VoteBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    """
    Endpoint to vote for a blog post.
    """
    request.user_id = current_user.id
    return db_article.vote_article(db, request = request)

@router.post('/image')
def upload_image(image: UploadFile = File(...)
                #  , db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)
                 ):
    """
    Endpoint to upload an image for a blog post.
    """
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(10))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {"filename": path}