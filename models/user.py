from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Text
from config.db import meta, engine

users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('email', String(255)),
    Column('phone', String(255)),
    Column('password', String(255)),
)

posts = Table(
    'posts', meta,
    Column('id', Integer, primary_key=True),
    Column('caption', Text),
    Column('owner_id', Integer, ForeignKey("users.id"))
)

meta.create_all(engine)
