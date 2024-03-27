import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from models import create_tables, User, Person, Photo
from config import DSN


engine = sq.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()


def check(item):
    # Проверка на user, person или photo в бд
    if isinstance(item, User):
        for user in session.query(User).all():
            if user.vk_id == item.vk_id:
                return True
    elif isinstance(item, Person):
        for person in session.query(Person).all():
            if person.vk_id == item.vk_id:
                return True
    elif isinstance(item, Photo):
        for photo in session.query(Photo).all():
            if photo.vk_link == item.vk_link:
                return True
    return False


def add_info(item):
    # Добавление user или person в бд
    if check(item):
        session.close()
        return
    session.add(item)


def add_photo(photo: Photo):
    # Добавление фото в бд
    if check(photo):
        return
    session.add(photo)


def like_list() -> list:
    # Получение избранных в виде [person, [person_photos]]
    result = []
    for p in session.query(Person).join(Photo.person).filter(Person.like):
        photo_list = []
        for i in session.query(Photo).join(Person.photos).filter(Photo.person_vk_id == p.vk_id):
            photo_list.append(i)
        result.append([p, photo_list])
    return result


def get(vk_id: int, model):
    # Получение user или person из бд
    return session.query(model).filter(model.vk_id == vk_id).first()


def change_is_favourite(vk_id: int):
    # Изменение статуса like
    person = session.query(Person).filter(Person.vk_id == vk_id)
    if not person.first().like:
        person.update({Person.like: True})
    else:
        person.update({Person.like: False})
    session.commit()


def commit_session():
    session.commit()


def close_session():
    session.close()