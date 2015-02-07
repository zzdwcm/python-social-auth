#coding:utf8
# author:duoduo3369@gmail.com  https://github.com/duoduo369
"""
Weixin OAuth2 backend, docs at:
"""
from requests import HTTPError

from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthCanceled, AuthUnknownError


class WeixinMPOAuth2(BaseOAuth2):
    """Weixin MP OAuth authentication backend"""
    name = 'weixin_mp'
    ID_KEY = 'openid'
    AUTHORIZATION_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize'
    AUTHORIZATION_URL_ANCHOR = "wechat_redirect"
    ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    ACCESS_TOKEN_METHOD = 'GET'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('nickname', 'username'),
        ('headimgurl','profile_image_url'),
        ('unionid', 'unionid'),
    ]

    def get_user_details(self, response):
        """Return user details from Weixin. API URL is:
        https://api.weixin.qq.com/sns/userinfo
        """
        if self.setting('DOMAIN_AS_USERNAME'):
            username = response.get('domain', '')
        else:
            username = response.get('nickname', '')
        profile_image_url = response.get('headimgurl', '')
        return {'username': username, 'profile_image_url': profile_image_url}

    def user_data(self, access_token, *args, **kwargs):
        data = self.get_json('https://api.weixin.qq.com/sns/userinfo',
                             params={'access_token': access_token,
                                     'openid': kwargs['response']['openid'],
                                     'lang':'zh_CN'})
        nickname = data.get('nickname')
        if nickname:
            # 微信蛇精病的接口，返回的是一个奇怪的东西
            data['nickname'] = nickname.encode('raw_unicode_escape').decode('utf-8')
        return data

    def auth_params(self, state=None):
        appid, secret = self.get_key_and_secret()
        params = {
            'appid': appid,
            'redirect_uri': self.get_redirect_uri(state),
            'scope': 'snsapi_userinfo',
        }
        if self.STATE_PARAMETER and state:
            params['state'] = state

        if self.RESPONSE_TYPE:
            params['response_type'] = self.RESPONSE_TYPE
        return params

    def auth_complete_params(self, state=None):
        appid, secret = self.get_key_and_secret()
        return {
            'grant_type': 'authorization_code',  # request auth code
            'code': self.data.get('code', ''),  # server response code
            'appid': appid,
            'secret': secret,
            #'redirect_uri': self.get_redirect_uri(state),
        }

    def refresh_token_params(self, token, *args, **kwargs):
        appid, secret = self.get_key_and_secret()
        return {
            'refresh_token': token,
            'grant_type': 'refresh_token',
            'appid': appid,
            #'secret': secret
        }

