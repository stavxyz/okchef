# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Client for Chef API."""

import requests

import chef


class ChefClientSession(requests.Session):

    """A session with persistent parameters."""

    def __init__(self):
        super(ChefClientSession, self).__init__()
        self.headers['Accept'] = 'application/json'
        self.headers['Content-Type'] = 'application/json'


class ChefClient(object):

    """Client to the Chef API.

    Most calls will require authorization. Use the authenticate()
    method to authorize this client's session.
    """

    def __init__(self, endpoint, version='12.0.2'):

        endpoint = endpoint
        self.version = version
        self.endpoint = endpoint.strip().rstrip(' /')
        self._session = None
        self._http_adapter = None
        self.user_id = None

    def __repr__(self):
        """Show client instance."""
        rpr = "<ChefClient('%s')" % self.endpoint
        if self.auth:
            rpr += ' auth=%r' % self.auth
        rpr += '>'
        return rpr

    @property
    def auth(self):
        """Return the session's auth value."""
        return self.session.auth

    @property
    def session(self):
        """Return this client's session."""
        if not self._session:
            self._session = ChefClientSession()
            self._session.headers['X-Chef-Version'] = self.version
            # TODO(sam): add version to user-agent and see if requests will
            #            accept a list of strings as a header.
            self._session.headers['User-Agent'] = (
                "%s %s"
                % ('python/OkChef', self._session.headers['User-Agent']))
            self._http_adapter = requests.adapters.HTTPAdapter(
                pool_connections=100, pool_maxsize=100, max_retries=2)
            self._session.mount(self.endpoint, self._http_adapter)
        return self._session

    def authenticate(self, user_id, private_key):
        auth = chef.mixlib_auth.HttpChefMixlibAuth(user_id, private_key)
        self.session.auth = auth
        self.user_id = user_id
        return auth

    def get_version(self):
        """Return the version object from the server."""
        return self.get('/version').json()

    def _caturl(self, path):
        path = path.strip().lstrip(' /')
        return '%s/%s' % (self.endpoint, path)

    def get(self, path, **kwargs):
        """Perform a GET request."""
        url = self._caturl(path)
        return self.session.get(url, **kwargs)

    def post(self, path, **kwargs):
        """Perform a POST request."""
        url = self._caturl(path)
        return self.session.post(url, **kwargs)

    def delete(self, path, **kwargs):
        """Perform a DELETE request."""
        url = self._caturl(path)
        return self.session.delete(url, **kwargs)

    def options(self, path, **kwargs):
        """Perform an OPTIONS request."""
        url = self._caturl(path)
        return self.session.options(url, **kwargs)

    def head(self, path, **kwargs):
        """Perform a HEAD request."""
        url = self._caturl(path)
        return self.session.head(url, **kwargs)

    def patch(self, path, **kwargs):
        """Perform a PATCH request."""
        url = self._caturl(path)
        return self.session.patch(url, **kwargs)
