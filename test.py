import vk_api
from datetime import datetime


class VK_Parser:
    def __init__(self, token: str):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()


    def getPosts(self, query: list, count: int):
        try:
            unique = list()
            posts = self.vk.vk.wall.search(q=query, count=200)
            for post in posts["items"]:
                text = post["text"]
                if not(text in [u["text"] for u in unique]):
                    unique.append(post)
                else:
                    print("un xif")
            return unique
        except vk_api.ApiError as e:
            print(f"Error{e}")

    def getForTextList(self, posts):
        res_set = set()
        try:
            for post in posts:
                text = post["text"]
                date = datetime.fromtimestamp(post["date"])
                res_set.add(text)
        except vk_api.ApiError as e:
            print(f"Ошибка: {e}")
        return res_set


    def retImages(self, posts):
        for post in posts:
            text = post["text"]
            date = datetime.fromtimestamp(post["date"])
            print(post)
            try:
                if post["attachments"][0]["type"] == "photo":
                    pass
                    # print(post["attachments"][0]["photo"]["sizes"])
            except KeyError as ke:
                print(ke)
            except IndexError as ie:
                print(ie)




VK_TOKEN = input("В целях безопасности тут нет ключа:")
search_query = "neimark_it"
count = 100

parser = VK_Parser(token=VK_TOKEN)
posts = parser.getPosts(search_query, count)
texts = parser.getForTextList(posts)
print(texts)
print(parser.retImages(posts))
