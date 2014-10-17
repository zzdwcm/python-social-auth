#coding:utf8
# author:duoduo3369@gmail.com  https://github.com/duoduo369
"""
RenRen OAuth2 backend, docs at:
"""
from social.backends.oauth import BaseOAuth2


class RenRenOAuth2(BaseOAuth2):
    """RenRen (of sina) OAuth authentication backend"""
    name = 'renren'
    ID_KEY = 'id'
    AUTHORIZATION_URL = 'https://graph.renren.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://graph.renren.com/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('name', 'username'),
    ]

    def get_user_details(self, response):
        """Return user details from RenRen. API URL is:
        https://api.renren.com/v2/user/get
        """
        if self.setting('DOMAIN_AS_USERNAME'):
            username = response.get('domain', '')
        else:
            username = response.get('name', '')
        return {'username': username,}

    def user_data(self, access_token, *args, **kwargs):
        return kwargs['response']['user']
