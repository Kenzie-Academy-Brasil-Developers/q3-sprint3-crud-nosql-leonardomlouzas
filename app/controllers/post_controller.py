from http import HTTPStatus
from flask import jsonify, request
from app.models.post_model import Post


def get_posts():
    post_list = list(Post.get_all())

    for post in post_list:

        Post.serialize_post(post)

    return jsonify(post_list), HTTPStatus.OK


def get_post(post_id: int):
    post = Post.get_one(int(post_id))
    if not post:
        return {"error": f"Post {post_id} not found"}, HTTPStatus.NOT_FOUND

    return Post.serialize_post(post), HTTPStatus.OK


def create_post():
    data = request.get_json()

    if (
        not "title" in data
        or not "author" in data
        or not "tags" in data
        or not "content" in data
    ):
        return {"error": "Missing keys"}, HTTPStatus.BAD_REQUEST

    post = Post(data["title"], data["author"], data["tags"], data["content"])
    post.create_post()

    serialized_post = Post.serialize_post(post)

    return serialized_post.__dict__, HTTPStatus.CREATED


def remove_post(post_id: int):
    deleted_post = Post.delete_post(int(post_id))

    if not deleted_post:
        return {"error": f"Post {post_id} not found"}, HTTPStatus.NOT_FOUND

    Post.serialize_post(deleted_post)

    return deleted_post, HTTPStatus.OK


def patch_post(post_id: int):
    data = request.get_json()

    if (
        not "title" in data
        and not "author" in data
        and not "tags" in data
        and not "content" in data
    ):
        return {"error": "Missing keys"}, HTTPStatus.BAD_REQUEST

    if not Post.get_one(int(post_id)):
        return {"error": f"Post {post_id} not found"}, HTTPStatus.NOT_FOUND

    patched_post = Post.patch_post(int(post_id), data)

    if "error" in patched_post.keys():
        return patched_post, HTTPStatus.BAD_REQUEST

    patched_post = Post.get_one(int(post_id))
    patched_post = Post.serialize_post(patched_post)

    return patched_post
