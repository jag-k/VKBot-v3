from typing import List
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import SETTINGS, Permission
from modules.bot import Bot

func_type = type(lambda: True)


class Method:
    all_methods = []
    methods_by_code = {}  # type: {int: [Method]}

    def __init__(self, *codes: int,
                 func: func_type=None,
                 requirement: func_type=None,
                 permission=Permission.EVERYONE):
        self.codes = codes
        for code in codes:
            if code not in self.methods_by_code:
                self.methods_by_code[code] = [self]
            else:
                self.methods_by_code[code].append(self)

        self.func = None
        self.set_func(func)

        self.req = (lambda event: True) if requirement is None else requirement
        self.permission = permission

    def set_func(self, func: func_type):
        self.func = func
        return func

    @classmethod
    def add(cls, *codes: int, requirement: func_type=lambda event: True):
        def decorate(func: func_type):
            return Method(*codes, func=func, requirement=requirement)
        return decorate

    @classmethod
    def event(cls, event: vk_api.longpoll.Event, api):
        if event.type in Method.methods_by_code:
            return [method.func(Bot(api, event)) for method in filter(lambda m: type(m.func) == func_type and
                                           (Permission.have_access(m.permission, event.user_id) or
                                            event.from_me) and
                                           m.req(event),
                                 Method.methods_by_code[event.type])]
        return []


class Command(Method):
    commands = []

    def __init__(self, *commands: str, func: func_type=None,
                 command_characters: str=SETTINGS['bot_settings']['command characters'],
                 permission=Permission.ALLOWED):
        self.chars = list(map(lambda x: x.strip(), command_characters.split(',')))
        self.commands = commands
        Command.commands.append(self)

        super().__init__(
            VkEventType.MESSAGE_NEW,
            func=func,
            requirement=lambda event: any(event.text.startswith(char + cmd) for char in self.chars for cmd in commands),
            permission=permission
        )

    def set_func(self, func: func_type):
        def decorate(bot: Bot):
            bot.like_bot = True
            res = raw_res = func(bot)

            if res:
                if type(res) is tuple and len(res) == 2:
                    bot.like_bot = bool(res[1])
                    res = res[0]
                bot.send_feedback(res, bot.like_bot)
            return raw_res

        decorate.__doc__ = func.__doc__ or None
        self.func = decorate
        return decorate

    @classmethod
    def add(cls, *commands: str, command_characters: str=SETTINGS['bot_settings']['command characters'],
            permission=Permission.ALLOWED):
        def decorate(func: func_type):
            return Command(*commands, func=func, command_characters=command_characters, permission=permission)
        return decorate

    @property
    def help(self):
        return {
            "doc": self.func.__doc__.strip() if type(self.func) == func_type and
                                                self.func.__doc__ is not None else None,  # type: str
            "commands": self.commands,  # type: List[str],
            "permission": self.permission
        }


