import hashlib
import json
from datetime import datetime
import asyncio
import requests
import vk_api
from yandex_gpt import YandexGPT, YandexGPTConfigManagerForAPIKey
import yandex_gpt

import t_promt


class VK_Parser:
    """Парсер постов из групп VK по ключевому слову"""
    def __init__(self, token: str):
        """Инициализация парсера по серверному ключу доступа VK (https://dev.vk.com/ru/api/access-token/getting-started)"""
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()

    def getPostsByOwnerId(self, query: list, owner_id: str, count=100):
        """Получение списка постов по id групп
        Обратите внимание, идентификатор сообщества в параметре owner_id необходимо указывать со знаком «-» — например, owner_id = -1.

        *Пробивать по имени не удалось из-за прав доступа ключа*"""
        return self.vk.wall.search(owner_id=owner_id, query=query, count=count)

class YA_GPT:
    """Клас обложка для YandexGPT"""
    def __init__(self, model_type: str, catalog_id: str, api_key: str):
        """Инициализация по catalog_id(https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id?utm_referrer=https%3A%2F%2Fyandex.ru%2F) и api_key(https://yandex.cloud/ru/docs/foundation-models/quickstart/yandexgpt)"""
        config = YandexGPTConfigManagerForAPIKey(model_type=model_type, catalog_id=catalog_id, api_key=api_key)
        self.gpt = YandexGPT(config_manager=config)

    async def returnDictOnRequest(self, promt: str, text: str,):
        """Выводит словарь из промта и текста"""
        messages = [{"role": "system", "text": promt}, {"role": "user", "text": text}]
        completion = await self.gpt.get_async_completion(messages=messages, timeout=30)

        return json.loads(completion[completion.index("[")+1:completion.index("]")])


async def post_completion(post, url, GPT: YA_GPT):
    img_url, data = [None] * 2
    post_url = f"https://vk.com/{GROUP_ID}?w=wall{post['owner_id']}_{post['id']}"
    try:
        jst = await GPT.returnDictOnRequest(PROMT, post["text"])

        if post["attachments"][0]["type"] == "photo":
            img_url = post["attachments"][0]["photo"]["sizes"][-1]["url"]
        if img_url == None:
            raise Exception
        if "hash" in post.keys():
            uid = post["hash"]
        else:
            uid = hashlib.sha256(post["text"].encode()).hexdigest()


        data = {
            'title': jst["title"],
            'about': jst.get("about"),
            'period': jst["time"],
            'image': img_url,
            'id': uid,
            'categories': jst["categories"],
            'is_passed': jst["is_passed"],
            'url': post_url,
            'region': jst["region"]
        }
        print(data)
        # response = requests.post(url, data=data)
        # print(response.text)

    except Exception as e:
        print("e " + e.__str__())



VK_TOKEN = "5e97aac55e97aac55e97aac5855db5b97555e975e97aac53988ce9d07348f71675bf12a"
GROUP_ID, QUERY, COUNT = "yandex_education", "IT", 100
MODEL_TYPE, CATALOG_ID, API_KEY = "yandexgpt", "b1gukhevebno8l2921eu", "AQVN0kIl5D3-ks-_GzGiJ87GdDzBCQOP7Z5lTRUp"
SITE_TO_POST_URL = "http://gimnazevent.ru/NN/SendToBD.php/"
PROMT = t_promt.promt

VK_Pars = VK_Parser(VK_TOKEN)
search_results = VK_Pars.getPostsByOwnerId(owner_id=GROUP_ID, query=QUERY, count=COUNT)
GPT = YA_GPT(model_type=MODEL_TYPE, catalog_id=CATALOG_ID, api_key=API_KEY)

for post in search_results['items']:
    asyncio.run(post_completion(post, SITE_TO_POST_URL, GPT))
