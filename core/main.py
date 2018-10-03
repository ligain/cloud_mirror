import aiohttp_jinja2
import jinja2
from aiohttp import web
from core.routes import urls
from core.settings import config


async def create_app():
    app = web.Application()
    app.add_routes(urls)
    app['config'] = config
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('core', 'templates'))
    app['static_root_url'] = '/static'
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(
        app,
        host=config.get('host', ''),
        port=config.get('port', 8080),
    )