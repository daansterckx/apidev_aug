# crud.py
from sqlalchemy.orm import Session
import models, schemas

def get_movie_by_id(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movies(db: Session):
    return db.query(models.Movie).all()

def create_attendee(db: Session, attendee: schemas.AttendeeCreate, movie_id: int):
    db_attendee = models.Attendee(**attendee.dict(), movie_id=movie_id)
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee