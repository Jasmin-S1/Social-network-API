from pydantic import BaseSettings # za validaciju environment varijabli

class Settings(BaseSettings):
    database_hostname: str      # praksa je da env. varijable budu velikim slovima ali ce pydantic automatski konvertovati u velika slova
    database_port: str
    database_password: str  
    database_name: str 
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:         # import env. varijabli iz .env fajla
        env_file = ".env"
 
settings = Settings()