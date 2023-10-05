from typing import Optional
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    name: str
    email: str
    login_method: int

class BookBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    pages: float
    publisher: str
    url: Optional[str]
    isbn: Optional[str]
    isbn13: Optional[str]
    year_published: float
    is_ebook: Optional[bool] = False
    cover_page: Optional[str] = None
    average_rating: Optional[float] = 0
    number_of_ratings: Optional[int] = 0

class Book(BookBase, table=True):
    title_without_series: str
    modified_title: Optional[str]
    modified_publisher: Optional[str]