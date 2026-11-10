from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DB_URL = 'postgresql+psycopg://sd4:sd4@localhost:5432/insta_practice'
engine = create_engine(DB_URL, echo=True)

app = FastAPI()
templates = Jinja2Templates(directory='templates')

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]

def get_db():
    with Session(engine) as db:
        yield db

@app.get('/posts')
def post_list(request: Request, db: Session = Depends(get_db)):
    # with Session(engine) as db:
    posts = db.scalars(select(Post)).all()
    return templates.TemplateResponse(
        request=request,
        name='list.html',
        context={'posts':posts}
    ) 