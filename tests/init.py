from fastapi_sql import SQLAlchemy
from asyncio import run
from fastapi import FastAPI
from uvicorn import Server, Config
from os import path

app = FastAPI()

db = SQLAlchemy(app=app, database_uri='postgresql+asyncpg://postgres:postgres@localhost:5432/db-fastapi-sql')

class User(db.Model): # type: ignore
    __tablename__ = '__user__'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(16))
    
class Role(db.Model): #type: ignore
    __tablename__ = 'role'
    id = db.Column('id', db.Integer(), primary_key=True)
   
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('__user__.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)
   
run(db.create_all())
if not path.exists('migrations'):
    db.migration.init() 

if not db.migration.check():
    db.migration.revision()
    db.migration.upgrade()

server = Server(Config(app=app))
run(server.serve())
