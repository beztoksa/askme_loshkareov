from django.conf import settings
from cent.client.session import requests
from django.core.cache import cache
from app.models import Tag, Profile, Question
import jwt
import time

from app.views import question


def generate_token(user_id):
    token = jwt.encode({"sub": str(user_id), "exp": int(time.time()) + 10 * 60}, settings.CENTRIFUGO_HMAC_SECRET,
                       algorithm="HS256")
    return token


def is_login(request):
    is_login = request.user.is_authenticated
    if is_login:
        profile = request.user.profile
    else:
        profile = None
    return {'is_login': is_login, 'profile': profile}


def cenrifugo_context(request):
    token = generate_token(request.user.id)
    print(settings.CENTRIFUGO_URL)
    return {'token': token, 'ws_url': settings.CENTRIFUGO_URL}


def global_context(request):
    popular_tags = cache.get('popular_tags')
    popular_profiles = cache.get('popular_profiles')
    return {'popular_tags': popular_tags, 'popular_profiles': popular_profiles}
