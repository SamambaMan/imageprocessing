import logging
from aiohttp import web
from webapp.urls import build_urls


app = build_urls()
logging.basicConfig(level=logging.DEBUG)

web.run_app(app)
