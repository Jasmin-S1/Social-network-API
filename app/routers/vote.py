from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, database, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/votes",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id) # provjera dva uslova
    found_vote = vote_query.first()
    if(vote.direction == 1):
        if found_vote: # ako vec postoji vote onda ide HTTPException, ako nema onda se vote dodaje u bazu
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id) 
        db.add(new_vote)
        db.commit()
        return {"message": "Seccessfully added vote"}
    else:
        if not found_vote: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete()
        db.commit()
        return {"message": "Seccessfully deleted vote"}

