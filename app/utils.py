from passlib.context import CryptContext    # za hash-iranje passworda

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # za hash-ianje passworda (ovim se CryptContextu kasze koji je defaultni algoritam kriptiranja)

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hash_password):
    return pwd_context.verify(plain_password, hash_password)
