import vk_api
from config import vk_data

session = vk_api.VkApi(vk_data["login"], vk_data["password"])
session.auth()

api = session.get_api()  # type: vk_api.vk_api.VkApiMethod

if __name__ == '__main__':
    print(session.token)
