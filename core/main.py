import argparse
import aiohttp_jinja2
import aiohttp_session
import jinja2
from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from core.routes import urls
from core.settings import config
from core import db
from core.middlewares import user_auth_middleware


async def create_app():
    app = web.Application(
        middlewares=[
            aiohttp_session.session_middleware(
                EncryptedCookieStorage(config['secret_key'].encode())
            ),
            user_auth_middleware,
        ]
    )
    app.add_routes(urls)
    app['config'] = config
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('core', 'templates'))
    app['static_root_url'] = config['static_root_url']
    app.on_startup.append(db.init_db)
    app.on_cleanup.append(db.close_db)
    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Cloud mirror dev server"
    )
    parser.add_argument(
        '--host',
        help='Host to run dev server'
    )
    parser.add_argument(
        '-p', '--port',
        help='Port to run dev server'
    )
    parser.add_argument(
        '-r', '--reload',
        help='Automatically reload dev server on changes',
        action='store_true',
        default=False
    )
    init_settings = parser.parse_args()

    app = create_app()

    if init_settings.reload:
        try:
            import aioreloader
            aioreloader.start()
            print("Start dev server with autoreloader")
        except ImportError:
            print("Failed to start autoreloader")

    web.run_app(
        app,
        host=init_settings.host or config.get('host', ''),
        port=init_settings.port or config.get('port', 8080),
    )