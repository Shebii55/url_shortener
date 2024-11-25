from sqlalchemy.orm import Session
import models
from utils import generate_short_url

def create_url(db: Session, target_url: str):
    db_url = db.query(models.URL).filter(models.URL.target_url == target_url).first()
    if db_url:
        return db_url
    
    # Generate unique short URL and save to DB
    short_url = generate_short_url()
    db_url = models.URL(target_url=target_url, short_url=short_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_short_url(db: Session, short_url: str):
    return db.query(models.URL).filter(models.URL.short_url == short_url).first()
