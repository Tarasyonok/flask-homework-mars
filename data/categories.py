import sqlalchemy
import datetime
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "categories"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    hazard = sqlalchemy.Column(sqlalchemy.Integer)
    jobs = sqlalchemy.Column(sqlalchemy.String)
