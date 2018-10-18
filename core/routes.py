from aiohttp import web
from core import views


urls = [
    web.get('/', views.index, name='main_page'),
    web.get('/login', views.login),
    web.get('/google-auth2callback', views.google_drive_auth_callback, name='google_drive_auth_callback'),
    web.static('/static/', '../static', name='static'),
]