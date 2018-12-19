import configparser
import json

settings = configparser.ConfigParser()
settings.read("./data/settings.ini")

SETTINGS = {}
for key in settings:
    SETTINGS[key] = dict(settings[key])


secret = configparser.ConfigParser()
secret.read("./data/.secret/secret.ini")

SECRET = {}
for key in secret:
    SECRET[key] = dict(secret[key])

vk_data = SECRET.get('vk_data')


class Permission:
    EVERYONE = -1  # Доступно каждому
    ADMIN = 0  # Только для пользователя бота
    ADMINS = 1  # Практически полный доступ
    ALLOWED = 2  # Доступ частично разрешён

    NO_ACCESS = float("inf")  # Доступ запрещён

    @classmethod
    def have_access(cls, access_level, user_id: int):
        if access_level == cls.EVERYONE:
            return True

        users = dict([(u["user_id"], u['permission']) for u in cls().users])
        return users.get(user_id, cls.NO_ACCESS) <= access_level

    def add_user(self, user_id, access_level):
        data = self.users + [{
            "user_id": user_id,
            "permission": access_level
        }]
        json.dump(data, open("./data/permission.json", "w", encoding="utf-8"), indent=2)
        return data

    @property
    def users(self):
        return json.load(open("./data/permission.json", encoding="utf-8"))

    @classmethod
    def str_level(cls, access_level):
        return {
            cls.EVERYONE: "Любой пользователь",
            cls.ADMIN: "Владелец бота",
            cls.ADMINS: "Адмнинистраторы (приближённые)",
            cls.ALLOWED: "Некоторые пользователи",
            cls.NO_ACCESS: "Нет доступа"
        }.get(access_level, "Неизвестно")


if __name__ == '__main__':
    print(SETTINGS)
    print(SECRET)
