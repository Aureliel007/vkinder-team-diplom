import configparser

from vkbottle import API
from vkbottle.bot import BotLabeler, Message
from keyboards.keyborad import KEYBOARD_START_MENU, KEYBOARD_NEXT_MENU, KEYBOARD_MY_LIST

from db import check, add_info, commit_session, close_session, get_persons, get, Person, get_person_photos,\
    change_is_favourite, like_list

from .funcs import get_user_info, search_people, get_sex, get_person_info


labler = BotLabeler()
labler.vbml_ignore_case = True

vk_config = configparser.ConfigParser()
vk_config.read('config.ini')
vk_token = vk_config['vk']['token']
vk_group_id = vk_config['vk']['group_id']
vk_user_token = vk_config['vk']['user_token']

api = API(vk_token)
api_user = API(token=vk_user_token)

list_of_people = []
current = 0


@labler.message(text=['start', 'начать', 'привет', 'главное меню'])
async def bye_handler(message: Message):
    info = await message.get_user()

    await message.answer(f'Привет {info.first_name}!', keyboard=KEYBOARD_START_MENU)

    user = await get_user_info(api_user, info.id)
    global list_of_people

    if not check(user):  # проверка есть ли юзер в БД по vk_id
        add_info(user)
        await message.answer('Мы уже загружаем профили для вас, подождите немного!')
        # Ищем людей подходящих User исходя из данных его профиля
        people = await search_people(
                                     api_user,
                                     sex_id=get_sex(user.__getattribute__('sex_id')),
                                     city_id=user.__getattribute__('city_id'),
                                     age_from=user.__getattribute__('age')-5,
                                     age_to=user.__getattribute__('age')+5
                                     )
        # Записываем данные в БД
        await get_person_info(api_user, people.items, message.from_id, list_of_people)
        commit_session()
        await message.answer('Анкеты загружены!')
    else:  # Если user существует, загружаем всех у кого нет лайка
        if list_of_people:
            pass  # Заглушка, на случай если после вывода списка будет введены команды из данной функции
        else:

            data = get_persons(message.from_id)
            for person in data:
                list_of_people.append(person.vk_id)
            await message.answer('Анкеты загружены!')


@labler.message(text=['начать поиск', 'следующий', 'next'])
async def start_handler(message: Message):
    await message.answer("Сейчас посмотрим, кто у нас есть", keyboard=KEYBOARD_NEXT_MENU)

    global list_of_people
    global current

    if list_of_people:
        current = list_of_people.pop()
        result = get(current, Person)  # Достаём из списка последний ID и удаляем его как просмотренный
        data = get_person_photos(current)
        attachments = [link.vk_link for link in data]
        await message.answer(f'{result.first_name} {result.last_name}',
                             result.vk_link)
        await message.answer(attachment=','.join(attachments))  # Отправляем фото профиля

    else:
        await message.answer('К сожалению анкеты кончились...')
        data = get_persons(message.from_id)

        for person in data:
            list_of_people.append(person.vk_id)
        await message.answer('Мы загрузили анкеты, которые не были отмечены лайком.\n'
                             'Присмотритесь, может вы не заметили свою половинку:)')


@labler.message(text=['добавить в избранное'])
async def bye_handler(message: Message):
    global current
    if current == 0:
        await message.answer('Вы не начали поиск')
    else:
        change_is_favourite(current)
        await message.answer('Добавил', keyboard=KEYBOARD_NEXT_MENU)
        current = 0


@labler.message(text='мой список')
async def bye_handler(message: Message):
    favorite = like_list()
    await message.answer('Сейчас покажу весь твой избранный список!')
    for partner in favorite:
        await message.answer(f'{partner[0].first_name} {partner[0].last_name}',
                             partner[0].vk_link)
        await message.answer('-----------------------------------------')
    await message.answer('Готово!',
                         keyboard=KEYBOARD_MY_LIST)


@labler.message(text=['пока'])
async def bye_handler(message: Message):
    global list_of_people, current
    close_session()
    await message.answer('До встречи! Возвращайся скорее.')
