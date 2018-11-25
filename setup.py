import os
import sys

import vk_api

PATH = "data/.secret"

FILE = "secret.ini"

PATTERN = """[vk_data]
login=%s
password=%s"""

while True:
    login = input("Введите логин: ")
    pwd = input("Введите пароль: ")

    try:
        session = vk_api.VkApi(login, pwd)
        session.auth()

        api = session.get_api()

        break

    except Exception as err:
        print("ОШИБКА! Вы ввели не верные данные, повторите ввод", file=sys.stderr)

if not os.path.isdir(PATH):
    os.mkdir(PATH)

with open(os.path.join(PATH, FILE), 'w') as file:
    file.write(PATTERN % (login, pwd))
