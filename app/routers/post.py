from email import message
from fastapi import Depends, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app import oauth2
from .. import schemas, models
from ..database import get_db
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']     # za definisanje naslova i grupiranje u dokumentaciji (SwagerUI)
)


class Post(BaseModel):      
    title: str              
    content: str           
    published: bool = True  

@router.get("/")
def hello():
    return {"message": "Hello"}    

# @router.get("/", response_model=List[schemas.PostResponse]) kada se vracaju samo postovi
# @router.get("/", response_model=List[schemas.PostVotes]) # potrebno je dodati List, jer se vraca lista postova
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):           # bez List, response model je samo jedan post 
#     #posts = db.query(models.Post).all()                 # moramo specificirati da zelimo listu postova
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     # ako zelimo prikazati samo postove logovanog korisnika dodamo -> filter(models.Post.user_id == current_user.id) 

#     # JOIN operacije nad tabelama pomocu sqlalchemy (join votes tabele na posts tabelu)
#     posts_votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all() 
#     # count(votes.post_id) as votes i group by(post_id)
#     return posts_votes                                                                                                             
    
    # limit(limit vracenih postova), skip(preskoci prva dva), search(search based on keyword - title, content..) iznad su query parametri
    # ovi parametri idu nakon znaka ?
    # ako ih ima vise izmedju ide &  
    # % je znak za prazno mjesto u pretrazi
    
    
    
    



@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    post = db.query(models.Post).filter(models.Post.id == id).first()                                      
    if not post:                                                                                           
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")                                          
    return post  



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)  
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=current_user.id, **post.dict())     #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)                                               
    db.commit()
    db.refresh(new_post)
    return new_post



@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    if deleted_post.user_id != current_user.id:   # provjera da li je logovani user vlasnik posta
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")  
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found") 
    if post_query.first().user_id != current_user.id:   # provjera da li je logovani user vlasnik posta
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")  
    post_query.update(post.dict())
    db.commit()
    return post_query.first() 