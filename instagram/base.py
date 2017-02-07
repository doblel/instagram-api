"""oauth class."""
import requests


class InstagramBase(object):
    """Base class."""

    host = 'https://api.instagram.com'
    auth_path = '/oauth'

    def __init__(
        self,
        client_id=None,
        client_secret=None,
        redirect_uri=None,
        access_token=None
    ):
        """Initial args."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = access_token

    # https://www.instagram.com/developer/authentication/
    def auth_url(self, scope=('basic', 'public_content')):
        """Return instagram authorization url."""
        url = self.host + self.auth_path + '/authorize/?'
        scope = ' '.join(scope)
        p = 'client_id={}&redirect_uri={}&response_type=code&scope={}'.format(
            self.client_id,
            self.redirect_uri,
            scope
        )
        return url + p

    # https://www.instagram.com/developer/authentication/
    def exchange_code_for_token(self, code):
        """Get token from code."""
        url = self.host + self.auth_path + '/access_token'
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            'code': code
        }

        return self._make_request(method='POST', url=url, data=payload)

    # internal method
    def _make_request(self, method='GET', url=None, params=None, data=None):
        """Make request and return json representated response."""
        if method == 'GET':
            r = requests.get(url, params=params)
        elif method == 'POST':
            r = requests.post(url, data=data)
        else:
            r = requests.delete(url, params=params)

        if r.ok:
            data = r.json()
            return data
