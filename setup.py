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

import os

from setuptools import setup, find_packages

src_dir = os.path.dirname(os.path.realpath(__file__))

about = {}
with open(os.path.join(src_dir, 'chef', '__about__.py')) as abt:
    exec(abt.read(), about)

tests_require = [
    'vcrpy>=1.5.2',
]
dependencies = [
    'requests==2.7.0',
#    'cryptography>=0.10.dev9',
]
# cryptography==0.10.dev9 is not on pypi, so provide a link
dependency_links = [
#    ('https://github.com/samstav/cryptography'
#     '/tarball/rsa-bypass-hash-on-signer#egg=cryptography-0.10.dev9'),
]


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    license=about['__license__'],
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__email__'],
    tests_require=tests_require,
    dependency_links=dependency_links,
    test_suite='tests',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    install_requires=dependencies,
)
