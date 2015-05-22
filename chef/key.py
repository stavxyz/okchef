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

"""Auth module and private key utilities.

RSA public key-pairs are used to authenticate
the chef-client with the Chef server every
time a chef-client needs access to data that
is stored on the Chef server.

https://docs.chef.io/auth.html
"""

import os

from cryptography.hazmat import backends as crypto_backends
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

from chef import utils


class ChefClientRSAKey(object):

    """Requires an instance of RSAPrivateKey to initialize.

    The base class for this type is found in the crytography library
    at cryptography.hazmat.primitives.asymmetric.rsa
    """

    def __init__(self, private_key):

        import pdb; pdb.set_trace()
        # check isinstance with rsa module
        self.private_key = private_key

    @classmethod
    def load_pem(cls, private_key, password=None):
        """Return a PrivateKey instance.

        :param private_key: Private key string (PEM format) or the path
                            to a local private key file.
        """
        #TODO(sam): try to break this in tests
        maybe_path = utils.normpath(private_key)
        if os.path.isfile(maybe_path):
            with open(private_key, 'rb') as pkf:
                private_key = pkf.read()
        pkey = serialization.load_pem_private_key(
            private_key,
            password=password,
            backend=crypto_backends.default_backend())
        return type(cls)(pkey)

    def sign(self, data, base64=True):
        """Sign data with the private key and return the signed data.

        The signed data will be Base64 encoded if base64 is True.
        """
        padder = padding.PKCS1v15()
        signer = self.private_key.signer(padder, None)
        signer.update(data)
        signed = signer.finalize()
        if base64:
            signed = base64.b64encode(signed)
        return signed
