import openai
import vk_api
from datetime import datetime
import KEYS
import promt

# токен
vk_session = vk_api.VkApi(token="5e97aac55e97aac55e97aac5855db5b97555e975e97aac53988ce9d07348f71675bf12a")
vk = vk_session.get_api()


# Настройки для поиска
search_query = "IT конкурс", "хакатон", "IT мероприятие"
count = 100  # Количество постов для получения
wwq = set()
wwl = list()
def search_posts(query, count=10):
    try:
        posts = vk.newsfeed.search(q=query, count=count, start_time=int(datetime.now().timestamp()) - 864000)
        for post in posts["items"]:
            text = post["text"]
            date = datetime.fromtimestamp(post["date"])
            print(post)
            try:
                if post["attachments"][0]["type"] == "photo":
                    print(post["attachments"][0]["photo"]["sizes"])
            except KeyError as ke:
                print(ke)
            except IndexError as ie:
                print(ie)
            wwl.append(text)
            wwq.add(text)
    except vk_api.ApiError as e:
        print(f"Ошибка: {e}")

# Поиск и вывод результатов
search_posts(search_query, count)
# import yandexgptlite
# from yandexgptlite import YandexGPTLite
# GPT_KEYS = {"folder": "b1gukhevebno8l2921eu", "token": "y0_AgAAAABjBHlkAATuwQAAAAEWUdJQAADGmortblZNc5GNLZ3vYbDfaQwwAA"}
#
# account = YandexGPTLite(GPT_KEYS["folder"], GPT_KEYS["token"])
# text = account.create_completion(f"Привет, тебе будут поступать списки текста поств VK по тематике IT конкурсов тебе нужно преобразоать это в json в котором нужно указать временной интервал прохождения и кратко о конкурсе: {[wwq]}", 0.3)
#
# print(text)








from yandex_gpt import YandexGPT, YandexGPTConfigManagerForAPIKey

# Setup configuration (input fields may be empty if they are set in environment variables)
config = YandexGPTConfigManagerForAPIKey(model_type="yandexgpt", catalog_id="b1gukhevebno8l2921eu", api_key="AQVN0kIl5D3-ks-_GzGiJ87GdDzBCQOP7Z5lTRUp")

# Instantiate YandexGPT
yandex_gpt = YandexGPT(config_manager=config)
# Async function to get completion
async def get_completion(text):
    messages = [promt.promt, {"role": "user", "text": text}]
    completion = await yandex_gpt.get_async_completion(messages=messages, timeout=20)
    print(completion)


# Run the async function
import asyncio
asyncio.run(get_completion())
