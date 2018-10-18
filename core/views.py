import logging

import aiohttp_jinja2
import google_auth_oauthlib
from aiohttp.web_exceptions import HTTPServerError, HTTPFound, HTTPBadRequest
import google_auth_oauthlib.flow
from aiohttp_session import get_session
from oauthlib.oauth2 import InvalidGrantError

from core.utils import login_required
from core.settings import google_drive_secrets_file, modules_config


async def login(request):
    secrets_file = google_drive_secrets_file
    if not secrets_file:
        logging.error('Missing secrets file for google drive')
        raise HTTPServerError

    # prepare auth uri for google drive
    cfg = modules_config
    api_scopes = cfg.get('google_drive', {}).get('scopes', [])
    redirect_uri = request.url.parent.join(
        request.app.router['google_drive_auth_callback'].url_for()
    ).human_repr()
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        secrets_file, api_scopes, redirect_uri=redirect_uri)

    auth_url, state = flow.authorization_url(prompt='consent', access_type='offline')
    session = await get_session(request)
    session['google_drive_auth_state'] = state

    return aiohttp_jinja2.render_template(
        'login.html',
        request,
        {'google_drive_auth_url': auth_url}
    )


async def google_drive_auth_callback(request):
    session = await get_session(request)
    state = session.get('google_drive_auth_state', '')
    cfg = modules_config
    api_scopes = cfg.get('google_drive', {}).get('scopes', [])
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        google_drive_secrets_file, scopes=api_scopes, state=state)
    flow.redirect_uri = request.url.parent.join(
        request.app.router['google_drive_auth_callback'].url_for()
    ).human_repr()
    authorization_response = request.url.human_repr()
    try:
        flow.fetch_token(authorization_response=authorization_response)
    except InvalidGrantError:
        logging.exception("Error on getting google drive token: ")
        raise HTTPBadRequest()
    credentials = flow.credentials
    if credentials.valid:
        # create user here
        session['google_drive_credentials'] = {
            'access_token': credentials.token
        }
        raise HTTPFound(request.app.router['main_page'].url_for())
    raise HTTPBadRequest()

@login_required
async def index(request):
    session = await get_session(request)
    return aiohttp_jinja2.render_template('main_page.html', request, {})