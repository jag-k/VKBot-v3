from typing import List
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import SETTINGS, Permission
from modules.bot import Bot

function = type(lambda: True)


class Method:
    all_methods = []
    methods_by_code = {}  # type: {int: [Method]}

    def __init__(self, *codes: int,
                 func: function=None,
                 requirement: function=None,
                 permission=Permission.EVERYONE):
        self.codes = codes
        for code in codes:
            if code not in self.methods_by_code:
                self.methods_by_code[code] = [self]
            else:
                self.methods_by_code[code].append(self)

        self.func = func
        self.req = (lambda event: True) if requirement is None else requirement
        self.permission = permission

    def set_func(self, func: function):
        self.func = func

    @classmethod
    def add(cls, *codes: int, requirement: function=lambda event: True):
        def decorate(func: function):
            return Method(*codes, func=func, requirement=requirement)
        return decorate

    @classmethod
    def event(cls, event: vk_api.longpoll.Event, api):
        if event.type in Method.methods_by_code:
            for method in filter(lambda m: type(m.func) == function and
                                           (Permission.have_access(m.permission, event.user_id) or
                                            event.from_me) and
                                           m.req(event),
                                 Method.methods_by_code[event.type]):
                method.func(Bot(api, event))


# print(SETTINGS['bot_settings']['command characters'])


class Command(Method):
    commands = []

    def __init__(self, *commands: str, func: function=None,
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

    @classmethod
    def add(cls, *commands: str, command_characters: str=SETTINGS['bot_settings']['command characters'],
            permission=Permission.ALLOWED):
        def decorate(func: function):
            return Command(*commands, func=func, command_characters=command_characters, permission=permission)
        return decorate

    @property
    def help(self):
        return {
            "doc": self.func.__doc__.strip() if type(self.func) == function else None,  # type: str
            "commands": self.commands,  # type: List[str],
            "permission": self.permission
        }


