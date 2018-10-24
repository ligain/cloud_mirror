import logging

import aiohttp_jinja2
import google_auth_oauthlib
import httplib2
from aiohttp.web_exceptions import HTTPServerError, HTTPFound, HTTPBadRequest
import google_auth_oauthlib.flow
from aiohttp_session import get_session
from google.auth.transport.requests import AuthorizedSession
from googleapiclient.discovery import build
from oauthlib.oauth2 import InvalidGrantError

from core.db import User
from core.utils import login_required
from core.settings import google_drive_secrets_file, modules_config
from modules.google_drive.token_manager import GoogleDriveTokenManager


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
    if not credentials.valid:
        raise HTTPBadRequest()

    # create user here
    google_plus = build(
        'plus', 'v1', credentials=credentials)
    profile = google_plus.people().get(userId='me').execute()
    user = User(
        email=profile['emails'][0]['value'],
        username=profile.get('displayName', ''),
        profile_url=profile.get('url', ''),
        avatar_url=profile.get('image', {}).get('url', '')
    )
    await user.save_to_db(request.app['db'])
    session['userid'] = user.id
    tm = GoogleDriveTokenManager(
        access_token=credentials.token,
        refresh_token=credentials.refresh_token,
        expires=credentials.expiry,
        token_uri=credentials.token_uri,
    )
    raise HTTPFound(request.app.router['main_page'].url_for())

@login_required
async def index(request):
    session = await get_session(request)
    return aiohttp_jinja2.render_template('main_page.html', request, {})