from vkbottle import Keyboard, KeyboardButtonColor, Text


KEYBOARD_START_MENU = (
    Keyboard(one_time=True, inline=False)
    .add(Text('Начать поиск'), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Мой список"), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Пока"), color=KeyboardButtonColor.NEGATIVE)
)

KEYBOARD_NEXT_MENU = (
    Keyboard(one_time=True, inline=False)
    .add(Text('Следующий'), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Главное меню"), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Добавить в избранное"), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Пока"), color=KeyboardButtonColor.NEGATIVE)
)

KEYBOARD_MY_LIST = (
    Keyboard(one_time=True, inline=False)
    .add(Text('Начать поиск'), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Пока"), color=KeyboardButtonColor.NEGATIVE)
)
