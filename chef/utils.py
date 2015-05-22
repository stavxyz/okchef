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
"""Misc. utility functions."""

import os


def normpath(path):
    """Normalize a path.

    Expands ~'s, resolves relative paths, normalizes and returns
    an absolute path.
    """
    return os.path.abspath(os.path.normpath(os.path.expanduser(path)))


def splitter(iterable, chunksize=60):
    """Split an iterable that supports indexing into chunks of 'chunksize'."""
    return (iterable[0+i:chunksize+i]
            for i in range(0, len(iterable), chunksize))
