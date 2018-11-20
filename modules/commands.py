from .schemas import Command, Bot, Permission
from config import SETTINGS


@Command.add('?', 'h', "help", permission=Permission.EVERYONE)
def get_help(bot: Bot):
    """Эта комманда возвращает данные о других комммандах (сейчас вызвана)
    Другие комманды, для вывода информации о них (без аргументов выводит все)
    """

    func_off = list(map(lambda x: x.strip(), SETTINGS['functions']['off'].split(',')))

    def func_info(func_data):
        t = "• Комманда %s:%s\n" % (
            '; '.join(func_data['commands']),
            " ⚠ Комманда не работает! ⚠" if any(i in func_off for i in func_data['commands']) else '')

        d = func_data['doc'].split('\n') or ['']
        descrtiption, params = d[:1], d[1:]
        params, notes = params[:1], params[1:]

        t += "Без описания" if not descrtiption else descrtiption[0]

        t += "\n📝 " + ("Не имеет аргументов" if not params else params[0])
        t += "" if not notes else "\n⚠ Примечание: " + notes[0]

        t += "\n🔑 Уровень доступа: " + Permission.str_level(func_data["permission"])
        return t

    functions = list(map(lambda c: c.help, Command.commands))
    params = bot.event.text.split()[1:]

    cmds_keys = dict((key, i) for i in functions for key in i['commands'])

    res = []
    for i in params:
        if i in cmds_keys:
            res.append(func_info(cmds_keys[i]))

    res = res if res else map(func_info, functions)

    chars = list(map(lambda x: x.strip(), SETTINGS['bot_settings']['command characters'].split(',')))

    help_start = "Символ%s комманды по умолчанию: %s\n\n" % ("ы" if len(chars) > 1 else '',
                                                             '; '.join("%s (%scommand)" % (ch, ch) for ch in chars))

    return help_start + '\n\n'.join(res)


@Command.add('с', 'c', "connect", permission=Permission.ALLOWED)
def connect(bot: Bot):
    """проверка соединения
    """

    return "Connection success!"


@Command.add("id")
def get_id(bot: Bot):
    """Можно узнать свой User ID"""
    # print(bot.event.user_id)
    u_id = bot.event.user_id

    r = "%s, Ваш ID: %d\n\nhttps://vk.com/id%d" % (bot.reference(), u_id, u_id)
    print(r)
    return r


@Command.add("stop", permission=Permission.ADMIN)
def stop(bot: Bot):
    """Останавливает Бота"""

    bot.send_feedback("Бот остановлен")
    return bot.StopBot  # FIXME: Доделать остановку бота с комманды


# TODO: Сделать следующие комманды: list (список людей с их привелегиями), status (проверка своего статуса), add (добавить человека в список к "админам")
