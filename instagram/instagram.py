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
    def auth_url(self, scope='basic+public_content+follower_list+comments+likes'):
        """Return instagram authorization url."""
        url = self.host + self.auth_path + '/authorize/?'
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

    # https://www.instagram.com/developer/endpoints/users/#get_users_self
    def self(self, access_token=None):
        """Get information about the owner of the token."""
        url = self.api_path + '/users/self/?'
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/users/#get_users_media_recent_self
    def self_media(self, access_token=None):
        """Get the most recent media published by the owner of the token."""
        url = self.api_path + '/users/self/media/recent/?'
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/users/#get_users_feed_liked
    def self_media_liked(self, access_token=None):
        """Get the list of recent media liked by the owner of the token."""
        url = self.api_path + '/users/self/media/liked?'
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/users/#get_users
    def user_id(self, user_id, access_token=None):
        """Get information about a user."""
        url = self.api_path + '/users/{id}/?'.format(id=user_id)
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/users/#get_users_media_recent
    def user_media(self, user_id, access_token=None):
        """Get the most recent media published by a user."""
        url = self.api_path + '/users/{id}/media/recent/?'.format(id=user_id)
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request('GET', url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/users/#get_users_search
    def search_user(self, username, count=None, access_token=None):
        """Get a list of users matching the query."""
        url = self.api_path + '/users/search?'
        token = access_token if access_token else self.access_token
        payload = {
            'q': username,
            'count': count if count else 30,
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/relationships/#get_relationship
    def get_user_relationship(self, user_id, access_token=None):
        """Get information about a relationship to another user."""
        url = self.api_path + '/users/{id}/relationship?'.format(id=user_id)
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/relationships/#post_relationship
    def update_relationship(self, user_id, action, access_token=None):
        """Relationship endpoint.

        Modify the relationship between the current user and the target user.
        You need to include an action parameter to specify the relationship
        action you want to perform.
        Valid actions are: 'follow', 'unfollow' 'approve' or 'ignore'.
        """
        url = self.api_path + '/users/{id}/relationship?'.format(id=user_id)
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token,
            'action': action
        }

        return self._make_request(method='POST', url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/relationships/#get_users_follows
    def self_follows(self, access_token=None):
        """Get the list of users this user follows."""
        url = self.api_path + '/users/self/follows?'
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/relationships/#get_users_followed_by
    def self_followers(self, access_token=None):
        """Get the list of users this user is followed by."""
        url = self.api_path + '/users/self/followed-by?'
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/relationships/#get_incoming_requests
    def self_pending(self, access_token=None):
        """List the users who have requested this user's permission to follow."""
        url = self.api_path + '/users/self/requested-by?'
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/media/#get_media
    def get_media(self, media_id, access_token=None):
        """Media endpoint.

        Get information about a media object. Use the type field to.
        differentiate between image and video media in the response.
        You will also receive the user_has_liked field which tells you whether
        the owner of the access_token has liked this media.
        """
        url = self.api_path + '/media/{id}?'.format(id=media_id)
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/media/#get_media_search
    def search_media(self, location, access_token=None):
        """Search for recent media in a given area."""
        lat, lng = location
        url = self.api_path + '/media/search?'
        token = access_token if access_token else self.access_token
        payload = {
            'lat': lat,
            'lng': lng,
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/comments/#get_media_comments
    def media_comments(self, media_id, access_token=None):
        """Get a list of recent comments on a media object."""
        url = self.api_path + '/media/{id}/comments?'.format(id=media_id)
        token = access_token if access_token else self.access_token
        print token
        payload = {
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/comments/#post_media_comments
    def add_comment(self, media_id, comment, access_token=None):
        """Create a comment on a media object with the following rules.

        The total length of the comment cannot exceed 300 characters.
        The comment cannot contain more than 4 hashtags.
        The comment cannot contain more than 1 URL.
        The comment cannot consist of all capital letters.
        """
        url = self.api_path + '/media/{id}/comments'.format(id=media_id)
        token = access_token if access_token else self.access_token
        payload = {
            'text': comment,
            'access_token': token
        }

        return self._make_request(method='POST', url=url, data=payload)

    # https://www.instagram.com/developer/endpoints/comments/#delete_media_comments
    def remove_comment(self, media_id, comment_id, access_token=None):
        """Remove comment.

        Remove a comment either on the authenticated user's media object or
        authored by the authenticated user.
        """
        url = self.api_path + '/media/{id}/comments/{cid}?'.format(
            id=media_id,
            cid=comment_id
        )
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(method='DEL', url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/likes/#get_media_likes
    def media_likes(self, media_id, access_token=None):
        """Get a list of users who have liked this media."""
        url = self.api_path + '/media/{id}/likes?'.format(id=str(media_id))
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(url=url, params=payload)

    # https://www.instagram.com/developer/endpoints/likes/#post_likes
    def add_like(self, media_id, access_token=None):
        """Set a like on this media by the currently authenticated user."""
        url = self.api_path + '/media/{id}/likes'.format(id=str(media_id))
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(method='POST', url=url, data=payload)

    # https://www.instagram.com/developer/endpoints/likes/#delete_likes
    def remove_like(self, media_id, access_token=None):
        """Remove a like on this media by the currently authenticated user."""
        url = self.api_path + '/media/{id}/likes?'.format(id=str(media_id))
        token = access_token if access_token else self.access_token
        payload = {
            'access_token': token
        }

        return self._make_request(method='DEL', url=url, params=payload)

    # internal method
    def _make_request(self, method='GET', url=None, params=None, data=None):
        """Make request and return json representated response."""
        if method == 'GET':
            r = requests.get(url, params=params)
        elif method == 'POST':
            r = requests.post(url, data=data)
        else:
            r = requests.delete(url, params=params)

        print r.status_code, r.url
        if r.ok:
            data = r.json()
            return data
