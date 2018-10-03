import aiohttp_jinja2


@aiohttp_jinja2.template('main_page.html')
async def index(request):
    return {}