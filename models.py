import sqlalchemy as sq
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


def create_tables(engine):
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String(length=50), nullable=False)
    last_name = sq.Column(sq.String(length=50), nullable=False)
    age = sq.Column(sq.Integer, nullable=False)
    sex_id = sq.Column(sq.Integer, nullable=False)
    city = sq.Column(sq.String(length=50), nullable=False)


class Person(Base):
    __tablename__ = 'person'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String(length=50), nullable=False)
    last_name = sq.Column(sq.String(length=50), nullable=False)
    vk_link = sq.Column(sq.String(length=500), nullable=False)
    like = sq.Column(sq.Boolean)
    user_vk_id = sq.Column(sq.Integer, sq.ForeignKey("user.vk_id"), nullable=False)

    user = relationship(User, backref='person')


class Photo(Base):
    __tablename__ = 'photo'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_link = sq.Column(sq.String, unique=True)
    person_vk_id = sq.Column(sq.Integer, sq.ForeignKey("person.vk_id"), nullable=False)

    person = relationship(Person, backref='photos')
