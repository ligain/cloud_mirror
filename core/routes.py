from aiohttp import web
from core import views


urls = [
    web.get('/', views.index),
    web.static('/static/', '../static', name='static'),
]