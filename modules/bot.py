import math
from vk_api.longpoll import Event


class Bot:
    bot_string = "[id173996641|🐩 JksBot]: "

    def __init__(self, api, event: Event):
        self.api, self.event = api, event
        self.like_bot = True

    def send_feedback(self, text: str, like_bot: bool=None, *fwd_messages: int, **kwargs):
        like_bot = self.like_bot if like_bot is None else like_bot
        return self.api.messages.send(**kwargs,
                                      peer_id=self.event.peer_id,
                                      message=(self.bot_string if like_bot else '') + text,
                                      forward_messages=','.join(map(str, fwd_messages)),
                                      )

    def name(self, u_id=None, name_case="nom", full=False, try_count=0):
        """
        именительный – nom, родительный – gen, дательный – dat, винительный – acc, творительный – ins, предложный – abl.
        """
        try:
            if u_id is None:
                u_id = self.event.user_id

            if int(u_id) < 0:
                return self.api.groups.getById(group_id=-u_id)[0]['name']
            if u_id >= 2000000000:
                return self.api.messages.getChat(chat_id=u_id - 2000000000)['title']

            data = self.api.users.get(**{'user_ids': u_id, 'name_case': name_case})
            print("USER", data)
            data = data[0]

            return (data['first_name'] + ' ' + data['last_name']) if full else data['first_name']
        except Exception as err:
            if try_count < 3:
                return self.name(u_id, name_case, full, try_count + 1)
            return ''

    def reference(self, u_id=None, name_case="nom", full=False):
        if u_id is None:
            u_id = self.event.user_id
        return '[id%s|%s]' % (int(math.fabs(u_id)), self.name(u_id, name_case, full))
