from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime





class Post(BaseModel):      
    title: str              
    content: str           
    published: bool = True  


class CreatePost(BaseModel):      
    title: str              
    content: str           
    published: bool = True  


class UpdatePost(BaseModel):      
    title: str              
    content: str           
    published: bool




# mozemo imati posebno definisanu klasu za svaki od requesta

# mozemo i na drugaciji nacin definisati klase

class PostBase(BaseModel):         # all pydantic model always extend BaseModel
    title: str              
    content: str           
    published: bool = True  



class PostCreate(PostBase):    # ovu klasu treba i pozivati kod post i put metoda
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# definisanje pydantic modela za response 
class PostResponse(PostBase):    # sva ostala polja ce naslijediti iz klase PostBase 
    created_at: datetime      
    user_id: int
    user: UserResponse   # ovo polje ce sadrzavati informacije o user-u koji je kreirao post (referira se na klasu UserResponse)

    class Config:
        orm_mode = True


#definisanje response (pydantic) modela za join tabela posts i votes
class PostVotes(PostBase):  
    Post: PostResponse     # definisano je ovako jer query vraca dva polja, 1. Post i 2. votes, izgled response modela u fajlu example_join_tabela.py
    votes: int

    


class UserCreate(BaseModel):
    email: EmailStr          # Emailstr je email validator - provjerava da li je validan mail a ne neki random tekst
    password: str            # ne radi validacija email-a, ne moze da importuje email-validator

# kada pohranjujemo password u bazu ne pohranjujemo ga kao plain tekst, vec uradimo hash passworda
# potrebno je instalirati (pip install passlib[bcrypt])




class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)  # samo dvije opcije "les than" or "equal to" 1 (ako se lajkuje ide 1, ako ne onda  0)