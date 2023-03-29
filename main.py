from sqlalchemy import Column, Integer, String, create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from fastapi import FastAPI
from sqladmin import Admin, ModelView

Base = declarative_base()
engine = create_engine(
    "sqlite:///example.db",
    connect_args={"check_same_thread": False},
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True)
    author = Column(String)
    content = Column(String)


Base.metadata.create_all(engine)  # Create tables


app = FastAPI()
admin = Admin(app, engine)

class TweetAdmin(ModelView, model=Tweet):
    column_list = [Tweet.id, Tweet.content, Tweet.author]

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]


admin.add_view(UserAdmin)
admin.add_view(TweetAdmin)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/tweets")
async def say_tweets():
    session = Session(engine)
    return [tweet.content for tweet in session.scalars(select(Tweet))]
