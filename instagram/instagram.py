"""core."""
import requests


class Instagram(object):
    """Class that involves the methods of the instragram api."""

    host = 'https://api.instagram.com'
    base_path = '/v1'
    auth_path = '/oauth'
    api_path = host + base_path

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
    def auth_url(self, scope='basic+public_content+follower_list'):
        """Return instagram authorization url."""
        url = self.host + self.auth_path + '/authorize/?'
        url += 'client_id={}&redirect_uri={}&response_type=code&scope={}'.format(
            self.client_id,
            self.redirect_uri,
            scope
        )
        return url

    # https://www.instagram.com/developer/authentication/
    def exchange_code_for_token(self, code=None):
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

    # https://www.instagram.com/developer/endpoints/users/#get_users_self
    def self(self, access_token=None):
        """Get information about the owner of the token."""
        url = self.api_path + '/users/self/?'
        payload = {
            'access_token': access_token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/users/#get_users_media_recent_self
    def self_media(self, access_token=None):
        """Get the most recent media published by the owner of the token."""
        url = self.api_path + '/users/self/media/recent/?'
        payload = {
            'access_token': access_token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/users/#get_users_feed_liked
    def self_media_liked(self, access_token=None):
        """Get the list of recent media liked by the owner of the token."""
        url = self.api_path + '/users/self/media/liked?'
        payload = {
            'access_token': access_token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/users/#get_users
    def user_id(self, user_id=None, access_token=None):
        """Get information about a user."""
        url = self.api_path + '/users/{id}/?'.format(id=user_id)
        payload = {
            'access_token': access_token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/users/#get_users_media_recent
    def user_media(self, user_id=None, access_token=None):
        """Get the most recent media published by a user."""
        url = self.api_path + '/users/{id}/media/recent/?'.format(id=user_id)
        payload = {
            'access_token': access_token
        }

        return self._make_request('GET', url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/users/#get_users_search
    def search_user(self, username=None, count=None, access_token=None):
        """Get a list of users matching the query."""
        url = self.api_path + '/users/search?'
        payload = {
            'q': username,
            'count': count if count else 10,
            'access_token': access_token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/relationships/#get_relationship
    def get_user_relationship(self, user_id=None, access_token=None):
        """Get information about a relationship to another user."""
        url = self.api_path + '/users/{id}/relationship?'.format(id=user_id)
        payload = {
            'access_token': access_token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/relationships/#post_relationship
    def update_relationship(self, user_id=None, action=None, access_token=None):
        """
        Modify the relationship between the current user and the target user.
        You need to include an action parameter to specify the relationship
        action you want to perform.
        Valid actions are: 'follow', 'unfollow' 'approve' or 'ignore'.
        """
        url = self.api_path + '/users/{id}/relationship?'.format(id=user_id)
        payload = {
            'access_token': access_token,
            'action': action
        }

        return self._make_request(method='POST', url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/relationships/#get_users_follows
    def self_follows(self, access_token=None):
        """Get the list of users this user follows."""
        url = self.api_path + '/users/self/follows?'
        payload = {
            'access_token': access_token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/relationships/#get_users_followed_by
    def self_followers(self, access_token=None):
        """Get the list of users this user is followed by."""
        url = self.api_path + '/users/self/followed-by?'
        payload = {
            'access_token': access_token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/relationships/#get_incoming_requests
    def self_pending(self, access_token=None):
        """List the users who have requested this user's permission to follow."""
        url = self.api_path + '/users/self/requested-by?'
        payload = {
            'access_token': access_token
        }

        return self._make_request(url=url, params=payload)

    # internal method
    def _make_request(self, method='GET', url=None, params=None, data=None):
        """Make request and return json representated response."""
        if method == 'GET':
            r = requests.get(url, params=params)
        else:
            r = requests.post(url, data=data)

        if r.ok:
            data = r.json()
            return data
