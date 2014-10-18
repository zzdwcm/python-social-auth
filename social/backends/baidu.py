#coding:utf8
# author:duoduo3369@gmail.com  https://github.com/duoduo369
"""
Baidu OAuth2 backend, docs at:
"""
from social.backends.oauth import BaseOAuth2


class BaiduOAuth2(BaseOAuth2):
    """Baidu (of sina) OAuth authentication backend"""
    name = 'baidu'
    ID_KEY = 'userid'
    AUTHORIZATION_URL = 'http://openapi.baidu.com/oauth/2.0/authorize'
    ACCESS_TOKEN_URL = 'https://openapi.baidu.com/oauth/2.0/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('username', 'username'),
    ]

    def get_user_details(self, response):
        """Return user details from Baidu. API URL is:
        https://openapi.baidu.com/rest/2.0/passport/users/getInfo
        """
        if self.setting('DOMAIN_AS_USERNAME'):
            username = response.get('domain', '')
        else:
            username = response.get('uname', '')
        return {'username': username,}

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json('https://openapi.baidu.com/rest/2.0/passport/users/getInfo',params={'access_token': access_token})
