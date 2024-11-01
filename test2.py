import hashlib
import json

import requests
import vk_api

import promt

VK_TOKEN = input("В целях безопасности тут нет ключа:")
vk_session = vk_api.VkApi(token=VK_TOKEN, scope='groups, wall')
vk = vk_session.get_api()
# groups = vk.groups.search(q='НЕЙМАРК', count=10)
# group_ids = [group['id'] for group in groups['items']]
# print(groups)
owner_id = "yandex_education"
search_results = vk.wall.search(owner_id=owner_id, query='IT', count=100)

for item in search_results['items']:
    print(item)

from yandex_gpt import YandexGPT, YandexGPTConfigManagerForAPIKey
import yandex_gpt
# Setup configuration (input fields may be empty if they are set in environment variables)
config = YandexGPTConfigManagerForAPIKey(model_type="yandexgpt", catalog_id=input("В целях безопасности тут нет ключа каталога:"), api_key=input("В целях безопасности тут нет ключа:"))

# Instantiate YandexGPT
yandex_gpt = YandexGPT(config_manager=config)
# Async function to get completion

image_set = set()
image_list = list()
async def get_completion(post, url='http://gimnazevent.ru/NN/SendToBD.php/'):
    img_url = None
    data = None
    post_url = f"https://vk.com/{owner_id}?w=wall{post['owner_id']}_{post['id']}"
    print(post_url)
    try:
        messages = [promt.promt, {"role": "user", "text": post["text"]}]
        completion = await yandex_gpt.get_async_completion(messages=messages, timeout=30)
        jst = json.loads(completion[completion.index("[")+1:completion.index("]")])
        img_url = None

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
        print(completion)
        print(data["image"])
        image_set.add(data["image"])
        image_list.append(data["image"])
        response = requests.post(url, data=data)
        print(response.text)

    except Exception as e:
        print("e " + e.__str__())


# Run the async function
import asyncio
for post in search_results['items']:
    asyncio.run(get_completion(post))

print(len(image_set), len(image_list))
