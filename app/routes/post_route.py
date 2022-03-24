# from app.controllers.post_controller import get_posts, create_post
from app.controllers import post_controller


def post_route(app):
    @app.get("/posts")
    def read_posts():
        return post_controller.get_posts()

    @app.get("/posts/<post_id>")
    def read_post_by_id(post_id):
        return post_controller.get_post(post_id)

    @app.post("/posts")
    def create_post():
        return post_controller.create_post()

    @app.delete("/posts/<post_id>")
    def delete_post(post_id):
        return post_controller.remove_post(post_id)

    @app.patch("/posts/<post_id>")
    def update_post(post_id):
        return post_controller.patch_post(post_id)
