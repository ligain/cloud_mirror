from aiohttp import web


async def index(request):
    return web.Response(text="Welcome home!")


async def create_app():
    app = web.Application()
    app.router.add_get('/', index)
    return app


if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/', index)
    web.run_app(app, host='localhost', port=8080)