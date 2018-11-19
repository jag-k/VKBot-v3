import sys

import modules

from modules.auth import api, session, user_id
from modules.bot import Bot
from modules.schemas import Method
from vk_api.longpoll import VkLongPoll


longpoll = VkLongPoll(session)

print("Bot Started")
api.messages.send(message=Bot.bot_string + "Бот запущен", user_id=user_id)

try:
    for event in longpoll.listen():
        try:
            Method.event(event, api)
        except Exception as err:
            error_msg = "ERROR (%s): %s" % (type(err).__name__, err)
            print(err, file=sys.stderr)
            api.messages.send(message=Bot.bot_string + error_msg, user_id=user_id)
except ConnectionError:
    print("CONNECTION ERROR", file=sys.stderr)

api.messages.send(message=Bot.bot_string + "Бот остановлен", user_id=user_id)
print("Bot Stopped")
