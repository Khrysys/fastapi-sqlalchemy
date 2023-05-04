from fastapi_sql import SQLAlchemy
from asyncio import run
from fastapi import FastAPI
from uvicorn import Server, Config
from os import path

app = FastAPI()

db = SQLAlchemy(app=app, database_uri='postgresql+asyncpg://postgres:postgres@localhost:5432/db-fastapi-sql')

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)
class User(db.Model): # type: ignore
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(16))
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref='user_id'
    )
    
class Role(db.Model): #type: ignore
    __tablename__ = 'role'
    id = db.Column('id', db.Integer(), primary_key=True)
    users = db.relationship('User', secondary=roles_users, backref='role_id')
   
run(db.create_all())
if not path.exists('migrations'):
    db.migration.init() 

if not db.migration.check():
    db.migration.revision()
    db.migration.upgrade()

server = Server(Config(app=app))
run(server.serve())
