import aiohttp_jinja2

from core.utils import login_required


async def login(request):
    return aiohttp_jinja2.render_template('login.html', request, {})


@login_required
async def index(request):
    return aiohttp_jinja2.render_template('main_page.html', request, {})