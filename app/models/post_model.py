import pymongo
from typing import Union
from datetime import datetime
from bson.errors import InvalidId

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["kenzie"]


class Post:
    def __init__(self, title, author, tags, content) -> None:
        self.title = title
        self.author = author
        self.tags = tags
        self.content = content
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.id = Post.new_id()

    @staticmethod
    def serialize_post(post: Union["Post", dict]):
        if type(post) is Post:
            post.__delattr__("_id")

        if type(post) is dict:
            post.__delitem__("_id")

        return post

    @staticmethod
    def new_id():
        last_id = 0
        posts = list(db.posts.find())
        for post in posts:
            last_id = post["id"] if "id" in post else last_id

        return last_id + 1

    @staticmethod
    def get_all():
        return db.posts.find()

    @staticmethod
    def get_one(post_id):
        try:
            return db.posts.find_one({"id": post_id})
        except InvalidId:
            return None

    def create_post(self):
        db.posts.insert_one(self.__dict__)

    @staticmethod
    def delete_post(post_id: int):

        return db.posts.find_one_and_delete({"id": post_id})

    @staticmethod
    def patch_post(post_id: str, data: dict):

        prev_data = db.posts.find_one({"id": post_id})
        updated_data = {}

        if "author" in data:
            updated_data["author"] = data["author"]
            data.__delitem__("author")

        if "content" in data:
            updated_data["content"] = data["content"]
            data.__delitem__("content")

        if "tags" in data:
            updated_data["tags"] = data["tags"]
            data.__delitem__("tags")

        if "title" in data:
            updated_data["title"] = data["title"]
            data.__delitem__("title")

        if data:
            return {
                "error": "There are Wrong Keys in the request body.",
                "Wrong Keys": list(data.keys()),
                "Correct keys": ["author", "content", "tags", "title"],
            }

        updated_data = {"$set": updated_data}

        updated_post = db.posts.find_one_and_update(prev_data, updated_data)

        return updated_post
