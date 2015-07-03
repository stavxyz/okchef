"""tests for okchef."""
import copy
import hashlib
import json
import os
import unittest

import chef
import six

from six.moves.urllib import parse

import vcr


CASSETTE_LIB = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'vcrpy_cassettes')
assert os.path.isdir(CASSETTE_LIB), "Cassette library dir not found."
TEST_PEM = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'test.pem')
assert os.path.isfile(TEST_PEM), "Test PEM file not found."

TEST_NETLOC = 'test-chef-server.net'
TEST_URL = 'https://{}'.format(TEST_NETLOC)
TEST_USERNAME = 'test-chef-server-user'


def sha512_hex(data):
    if not data:
        return data
    hasher = hashlib.sha512()
    if not isinstance(data, six.binary_type):
        data = data.encode('utf-8')
    hasher.update(data)
    return hasher.hexdigest()


class TestChefClient(unittest.TestCase):

    def __init__(self, methodName, username=None, pem=None,
                 url=None, record_mode='none'):
        super(TestChefClient, self).__init__(methodName)
        self.username = username or TEST_USERNAME
        self.pem = pem or TEST_PEM
        self.url = url or TEST_URL
        self.record_mode = record_mode

    def setUp(self):
        self.vcr = vcr.VCR(cassette_library_dir=CASSETTE_LIB,
                           record_mode=self.record_mode,
                           before_record_request=self.before_record_request)
        self.okchef_client = chef.ChefClient(self.url)
        self.okchef_client.authenticate(self.username, self.pem)
        self.okchef_client.session.headers['Accept-Encoding'] = ''

    def before_record_request(self, request):
        # vcrpy isn't doing a very good job of giving us a copy here...
        # lets try harder...
        request_class = type(request)
        assert hasattr(request_class, '_from_dict')
        request = request_class._from_dict(
            copy.deepcopy(request._to_dict()))

        # chef api calls tend to have the username in the URI
        request.uri = request.uri.replace(
            self.okchef_client.user_id, TEST_USERNAME)

        # the following properties are derived from self.uri
        #   port, host, scheme, path, query, url, protocol
        # i.e. self.uri can be modified, the others cant
        parsed_uri = parse.urlparse(request.uri)
        request.uri = parse.ParseResult(
            scheme=parsed_uri.scheme,
            netloc=TEST_NETLOC,
            # path=sha512_hex(parsed_uri.path),
            path=parsed_uri.path,
            params=sha512_hex(parsed_uri.params),
            query=sha512_hex(parsed_uri.query),
            fragment=sha512_hex(parsed_uri.fragment)
        ).geturl()

        for hdr, val in request.headers.items():
            if 'x-ops-userid' in hdr.lower():
                request.headers[hdr] = TEST_USERNAME
            elif 'x-ops-authorization' in hdr.lower():
                request.headers[hdr] = sha512_hex(val)
            elif 'x-ops-content-hash' in hdr.lower():
                request.headers[hdr] = sha512_hex(val)

        assert request.host == 'test-chef-server.net'
        return request

    def test_list_user_orgs(self):

        def _br_res(response):
            body_string = response['body']['string']
            dbody = json.loads(body_string.decode('utf-8'))
            # we only need a small slice for testing
            dbody = sorted(dbody, key=lambda o: o['organization']['guid'])[:2]
            # TODO(sam): see what happens when a user
            #            tries to --record with no orgs online
            for org in dbody:
                self.assertEqual(list(org.keys()), ['organization'])
                for key, val in org['organization'].items():
                    org['organization'][key] = sha512_hex(val)
            response['body']['string'] = json.dumps(dbody).encode('utf_8')
            return response

        with self.vcr.use_cassette(path='list_user_orgs.yaml',
                                   before_record_response=_br_res):
            path = '/users/%s/organizations' % self.okchef_client.user_id
            response = self.okchef_client.get(path)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        for org in data:
            self.assertIn('organization', org)
            _org = org['organization']
            self.assertIn('guid', _org)
            self.assertIn('name', _org)
            self.assertIn('full_name', _org)

    def test_other(self):

        pass

    def not_me(self):

        pass


if __name__ == '__main__':
    """Provide an interface to easily re-record cassettes"""

    import argparse

    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument('--record', '-r', action='store_const',
                   dest='record_mode',
                   default='none', const='all',
                   help="Run tests with vcrypy record mode turned on")
    p.add_argument('--url', '-u', default='https://api.chef.io',
                   help="Url of chef server to record against")
    p.add_argument('--user', '-s',
                   help="Chef server user")
    p.add_argument('--pem', '-p',
                   help="Path to chef user PEM file")
    p.add_argument('--verbose', '-v', dest='verbosity',
                   default=1,
                   action='store_const', const=2,
                   help='Verbose output')
    p.add_argument('--quiet', '-q', dest='verbosity',
                   action='store_const', const=0,
                   help='Quiet output')
    p.add_argument('--failfast', '-f', dest='failfast',
                   default=False,
                   action='store_true',
                   help='Stop on first fail or error')
    p.add_argument('--buffer', '-b', dest='buffer',
                   action='store_true', default=False,
                   help='Buffer stdout and stderr during tests')

    args = p.parse_args()
    runwith = {
        'verbosity': args.verbosity,
        'failfast': args.failfast,
        'buffer': args.buffer,
    }
    if args.record_mode != 'none':
        if not all((args.url, args.user, args.pem)):
            p.error("--record requires --url, --user, and --pem")
        else:
            # unittest helps us automatically discover tests
            cls = TestChefClient
            tests = [
                cls(t._testMethodName, args.user, args.pem,
                    args.url, args.record_mode)
                for t in unittest.TestLoader().loadTestsFromTestCase(cls)
            ]
            suite = unittest.TestSuite(tests=tests)
            unittest.TextTestRunner(**runwith).run(suite)
    else:
        unittest.main(**runwith)
