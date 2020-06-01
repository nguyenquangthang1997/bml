from aiohttp import web
from handler import Handler
import aiohttp_cors
import logging

LOGGER = logging.getLogger(__name__)

app = web.Application()
# print(dir)
handler = Handler()

app.router.add_route('POST', "/synchronize", handler.synchronize)
app.router.add_route('POST', "/login", handler.login)
app.router.add_route('POST', "/account", handler.create_account)
app.router.add_route('POST', "/get", handler.get_data)

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

for route in list(app.router.routes()):
    cors.add(route)
