from fastapi_sql import SQLAlchemy
from asyncio import run
from fastapi import FastAPI

app = FastAPI()

db = SQLAlchemy(database_uri='postgresql+asyncpg://postgres:postgres@localhost:5432/db-fastinni')

class User(db.Model): # type: ignore
    __tablename__ = '__user__'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(16))
   
 
run(db.create_all())

