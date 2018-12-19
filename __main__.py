import sys
import traceback

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
            m = Method.event(event, api)
            if Bot.StopBot in m:
                raise SystemExit

        except Bot.StopBot:
            print("Admin stopped the bot", file=sys.stderr)
            break

        except BaseException as err:
            print('\n')
            traceback.print_exc()
            error_msg = "ERROR (%s): %s" % (type(err).__name__, err)
            api.messages.send(message=Bot.bot_string + error_msg, user_id=user_id)

except ConnectionError:
    print("CONNECTION ERROR", file=sys.stderr)

except KeyboardInterrupt or SystemExit:
    print("System Exit")

finally:
    api.messages.send(message=Bot.bot_string + "Бот остановлен (финальная отправка в лс)", user_id=user_id)
    print("Bot Stopped", file=sys.stderr)
