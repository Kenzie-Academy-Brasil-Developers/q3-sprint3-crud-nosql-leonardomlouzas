from app.routes.home_route import home_route
from app.routes.post_route import post_route


def init_app(app):
    home_route(app)
    post_route(app)
    