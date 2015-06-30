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

# pandoc --from=markdown_github --to=rst README.md --output=README.rst
readme = os.path.join(src_dir, 'README.rst')
if os.path.isfile(readme):
    with open(os.path.join(src_dir, 'README.rst')) as rdme:
        LONG_DESCRIPTION = rdme.read()
else:
    LONG_DESCRIPTION = ''


TESTS_REQUIRE = [
    'vcrpy>=1.5.2',
]


INSTALL_REQUIRES = [
    'requests-chef>=0.0.4',
    'requests>=2.7.0',
]


CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
    'Development Status :: 4 - Beta',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
]


package_attributes = {
    'name': about['__title__'],
    'description': about['__summary__'],
    'long_description': LONG_DESCRIPTION,
    'keywords': ' '.join(about['__keywords__']),
    'version': about['__version__'],
    'tests_require': TESTS_REQUIRE,
    'test_suite': 'tests',
    'install_requires': INSTALL_REQUIRES,
    'packages': find_packages(exclude=['tests']),
    'author': about['__author__'],
    'author_email': about['__email__'],
    'classifiers': CLASSIFIERS,
    'license': about['__license__'],
    'url': about['__url__'],
}


setup(**package_attributes)
