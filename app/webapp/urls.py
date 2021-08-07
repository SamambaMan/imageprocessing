# URLS is a common entrypoint for webapplications
# Makes your life easyer to coordinate services and dependencies
from aiohttp import web
from .services import process


def build_urls():
    app = web.Application()
    app.add_routes([
        web.post('/process', process)
    ])

    return app
