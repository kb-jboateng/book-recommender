from fastapi import Depends, FastAPI
from database import get_session
from models import BookBase
from recommender import recommend_books
from services import *
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/api/get-reader-recommendations/{user_id}", response_model=list[BookBase])
def user_recommendations(user_id: str, db: Session = Depends(get_session)):
    recommended_books = recommend_books(user_id)

    if len(recommended_books) > 0:
        return get_books(db, recommended_books)
    else:
        return []
