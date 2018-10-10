import aiohttp_jinja2
import jinja2
from aiohttp import web
from core.routes import urls
from core.settings import config

from core import db


async def create_app():
    app = web.Application()
    app.add_routes(urls)
    app['config'] = config
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('core', 'templates'))
    app['static_root_url'] = '/static'
    app.on_startup.append(db.init_db)
    app.on_cleanup.append(db.close_db)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(
        app,
        host=config.get('host', ''),
        port=config.get('port', 8080),
    )