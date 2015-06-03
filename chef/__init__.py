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

from __future__ import absolute_import

import os

from chef import mixlib_auth
from chef.client import ChefClient
from chef.__about__ import *  # noqa

__all__ = ['HOSTED_CHEF_API', 'ChefClient']

HOSTED_CHEF_APIS = ['https://api.chef.io', 'https://api.opscode.com']
HOSTED_CHEF_API = HOSTED_CHEF_APIS[0]
_HERE = os.path.dirname(os.path.realpath(__file__))
_HEAD_FILE = os.path.abspath(os.path.join(_HERE, os.pardir, '.git', 'HEAD'))


def _read_commit_dot_txt():
    commit_dot_txt = os.path.join(_HERE, 'commit.txt')
    if os.path.isfile(commit_dot_txt):
        with open(commit_dot_txt) as sha:
            return sha.read().strip()


def _read_commit(path):
    """Lookup HEAD (current checkout) commit hash.

    Falls back to reading commit.txt in this dir.
    """
    if not os.path.isfile(path):
        return _read_commit_dot_txt()
    with open(path) as head:
        headref = head.read().strip()
    if 'ref:' in headref:
        link = headref.partition('ref:')[-1].strip()
        follow = os.path.join(os.path.dirname(path), link)
        return _read_commit(follow)
    elif len(headref) == 40:
        return headref
    else:
        raise StandardError("Cannot read %s for HEAD sha-1." % path)


__commit__ = _read_commit(_HEAD_FILE)

