from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "test" or form_data.password != "test":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = "test"
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/movie", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    return crud.create_movie(db=db, movie=movie)

@app.get("/movies", response_model=List[schemas.Movie])
def get_movies(db: Session = Depends(get_db)):
    return crud.get_movies(db=db)

@app.get("/movie/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@app.post("/movie/{movie_id}/attendee", response_model=schemas.Attendee)
def add_attendee(movie_id: int, attendee: schemas.AttendeeCreate, db: Session = Depends(get_db)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return crud.create_attendee(db=db, attendee=attendee, movie_id=movie_id)

@app.get("/attendees", response_model=List[schemas.Attendee])
def get_attendees(db: Session = Depends(get_db)):
    return db.query(models.Attendee).all()

@app.get("/attendee/{attendee_id}", response_model=schemas.Attendee)
def get_attendee(attendee_id: int, db: Session = Depends(get_db)):
    db_attendee = db.query(models.Attendee).filter(models.Attendee.id == attendee_id).first()
    if db_attendee is None:
        raise HTTPException(status_code=404, detail="Attendee not found")
    return db_attendee

@app.delete("/movie/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(db_movie)
    db.commit()
    return db_movie

@app.delete("/attendee/{attendee_id}", response_model=schemas.Attendee)
def delete_attendee(attendee_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_attendee = db.query(models.Attendee).filter(models.Attendee.id == attendee_id).first()
    if db_attendee is None:
        raise HTTPException(status_code=404, detail="Attendee not found")
    db.delete(db_attendee)
    db.commit()
    return db_attendee
    @app.put("/movie/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = crud.get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_movie.title = movie.title
    db_movie.description = movie.description
    db.commit()
    db.refresh(db_movie)
    return db_movie
