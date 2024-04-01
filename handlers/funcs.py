from asyncio import sleep
from datetime import datetime
from vkbottle import API
from models import User, Person, Photo
from db import check, add_info, add_photo
from typing import Union


async def search_people(user_api: API, age_from=None, age_to=None, city_id=None, city_title=None, sex_id=0, status=6):

    response = await user_api.users.search(  # group_token is unavailable for this method users.search.
        sort=0,  # 1 — по дате регистрации, 0 — по популярности.
        city=city_id,
        hometown=city_title,
        sex=sex_id,  # 1— женщина, 2 — мужчина, 0 — любой (по умолчанию).
        status=status,  # 1 — не женат или не замужем, 6 — в активном поиске.
        age_from=age_from,
        age_to=age_to,
        has_photo=True,  # 1 — искать только пользователей с фотографией, 0 — искать по всем пользователям
        count=10,  # количество выдаваемых анкет, максимальное число - 1000
        fields=["can_write_private_message",  # может ли текущий пользователь отправить личное сообщение.
                "city",  # Информация о городе
                "domain",  # Короткий адрес страницы.
                "home_town"]  # Название родного города.
    )
    return response


def get_old(birthday: str) -> Union[int | None]:
    """
    This func returns actual user age if there is one
    :param birthday:
    :return: int
    """
    if birthday is None:
        return None
    bday = birthday.split('.')
    now_day = datetime.now()
    year_today = now_day.date().year
    month_today = now_day.date().month
    day_today = now_day.date().day
    years = year_today - int(bday[2])
    months = month_today - int(bday[1])
    if months < 0:
        years -= 1
    if months == 0:
        days = day_today - int(bday[0])
        if days < 0:
            years -= 1
    return years


def get_sex(sex: int) -> int:
    if sex == 2:
        return 1
    elif sex == 1:
        return 2
    else:
        return 0


async def get_person_info(api_user: API, people: list, user_id: int, list_of_people: list) -> None:
    """
    This func create personal list of vk users for user and add all available info about them
    :param list_of_people:
    :param api_user: class API
    :param people: list of users
    :param user_id:
    :return: None
    """
    for partner in people:  # Проходимся по списку анкет
        person = Person(
                         vk_id=partner.id,
                         first_name=partner.first_name,
                         last_name=partner.last_name,
                         vk_link=f'https://vk.com/id{partner.id}',
                         user_vk_id=user_id
                         )
        await sleep(0.2)
        if not check(person):  # проверяем есть ли анкета в БД

            list_of_people.append(partner.id)  # Добавляем в список ID, для отслеживания просмотренных анкет
            add_info(person)  # Добавляем анкету в БД
            links_photo = await get_photos(api_user, person.vk_id)  # формируем список из 3 фото по лайкам

            for link in links_photo:
                photo = Photo(
                              vk_link=link,
                              person_vk_id=person.vk_id
                              )

                add_photo(photo)  # Добавляем в БД


async def get_user_info(api_user: API, user_id: int) -> object:
    """
    This func returns information about user
    :param api_user: class API
    :param user_id: int
    :return: dict
    """

    request = await api_user.request('users.get', {'user_ids': user_id, 'fields': ['city', 'sex', 'bdate']})
    user = User(
        first_name=request.get('response')[0].get('first_name'),
        last_name=request.get('response')[0].get('last_name'),
        vk_id=request.get('response')[0].get('id'),
        city=request.get('response')[0].get('city').get('title'),
        city_id=request.get('response')[0].get('city').get('id'),
        sex_id=request.get('response')[0].get('sex', None),
        age=get_old(request.get('response')[0].get('bdate'))
    )
    return user


async def get_photos(api_user: API, user_id: int) -> list:
    """
    This func returns three links to person photos
    :param api_user: class API
    :param user_id: int
    :return: list
    """
    request_photo = await api_user.request('photos.get', {'owner_id': user_id,
                                                          'album_id': 'profile',
                                                          'extended': 1,
                                                          'photo_sizes': 0})

    photos = sorted(request_photo.get('response').get('items'),
                    key=lambda x: x.get('likes').get('count'),
                    reverse=True)[:3]

    three_photos = ['photo{}_{}'.format(photo.get('owner_id'), photo.get('id')) for photo in photos]
    return three_photos
