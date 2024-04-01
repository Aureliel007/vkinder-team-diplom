from vkbottle import API, BuiltinStateDispenser
from vkbottle.bot import BotLabeler
import configparser
import logging
from handlers import labelers
from vkbottle.bot import Bot

labeler = BotLabeler()
state_dispenser = BuiltinStateDispenser()

logging.basicConfig(level=logging.INFO)
vk_config = configparser.ConfigParser()
vk_config.read('config.ini')
vk_token = vk_config['vk']['token']
vk_group_id = vk_config['vk']['group_id']

api = API(vk_token)
bot = Bot(token=vk_token)

for labeler in labelers:
        bot.labeler.load(labeler)


if __name__ == '__main__':
    bot.run_forever()
