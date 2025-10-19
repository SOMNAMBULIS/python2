from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Table, Column, func

from datetime import datetime

class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    



class UserOrm(Model):
    __tablename__ = 'user'
    
    
    name: Mapped[str]
    age: Mapped[int]


class QuestionOrm(Model):
    __tablename__ = 'Question'

    name : Mapped[str]
    answer : Mapped[str]
    opt1 : Mapped[str]
    opt2 : Mapped[str]
    opt3 : Mapped[str | None]

class Quize(Model):
    __tablename__ = 'quize'

    name : Mapped[str]
