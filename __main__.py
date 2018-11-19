import modules

from modules.auth import api, session
from modules.schemas import Method
from vk_api.longpoll import VkLongPoll


longpoll = VkLongPoll(session)

print("Bot Started")
for event in longpoll.listen():
    Method.event(event, api)

print("Bot Stopped")
