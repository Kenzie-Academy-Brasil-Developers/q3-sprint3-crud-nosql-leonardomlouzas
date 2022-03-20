import pymongo
from typing import Union
from datetime import datetime
from bson.errors import InvalidId
from bson.objectid import ObjectId

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

    @staticmethod
    def serialize_post(post: Union["Post", dict]):
        if type(post) is Post:
            post._id = str(post._id)

        if type(post) is dict:
            post.update({"_id": str(post["_id"])})

        return post

    @staticmethod
    def get_all():
        post_list = db.posts.find()

        return post_list

    @staticmethod
    def get_one(post_id):
        try:
            return db.posts.find_one({"_id": ObjectId(post_id)})
        except InvalidId:
            return None

    def create_post(self):
        db.posts.insert_one(self.__dict__)

    @staticmethod
    def delete_post(post_id: str):

        deleted_post = db.posts.find_one_and_delete({"_id": ObjectId(post_id)})

        return deleted_post

    @staticmethod
    def patch_post(post_id: str, data: dict):

        prev_data = db.posts.find_one({"_id": ObjectId(post_id)})

        updated_data = {}
        if "author" in data:
            updated_data["author"] = data["author"]

        if "content" in data:
            updated_data["content"] = data["content"]

        if "tags" in data:
            updated_data["tags"] = data["tags"]

        if "title" in data:
            updated_data["title"] = data["title"]

        updated_data = {"$set": updated_data}

        updated_post = db.posts.find_one_and_update(prev_data, updated_data)

        print(updated_post)

        return updated_post
