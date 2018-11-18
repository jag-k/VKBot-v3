import time

import modules
from modules.auth import api, session
from modules.schemas import Method
from vk_api.longpoll import VkLongPoll, VkEventType


from config import SETTINGS

longpoll = VkLongPoll(session)

print("Bot Started")
for event in longpoll.listen():
    Method.event(event, api)
    # print(event.type, event.text if event.type == VkEventType.MESSAGE_NEW else None)

print("Bot Stopped")
