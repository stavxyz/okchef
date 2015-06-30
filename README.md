# okchef
[![latest](https://img.shields.io/pypi/v/okchef.svg)](https://pypi.python.org/pypi/okchef)
[![Circle CI](https://circleci.com/gh/samstav/okchef.svg?style=svg)](https://circleci.com/gh/samstav/okchef)
[![Coverage Status](https://coveralls.io/repos/samstav/okchef/badge.svg?branch=master)](https://coveralls.io/r/samstav/okchef?branch=master)


```python

import chef

client = chef.ChefClient('https://api.opscode.com')
# not to be confused with chef-client, the agent :)
client.authenticate('chef-user', '~/chef-user.pem')
response = client.get('/users/chef-user')
response.json()
...
{'display_name': 'chef-user',
 'email': 'chef-user@example.com',
 'first_name': 'Chef',
 'last_name': 'User',
 'middle_name': '',
 'public_key': '-----BEGIN PUBLIC KEY-----\nMIIBIj...IDAQAB\n-----END PUBLIC KEY-----\n',
 'username': 'chef-user'}
```


#### Authentication & Authorization

`okchef` uses the auth handler from the `requests-chef` library at https://github.com/samstav/requests-chef


### Install

Before installing `okchef`, see the current installation instructions for `requests-chef`: https://github.com/samstav/requests-chef#install

If you don't feel like reading those, you can use `--process-dependency-links` (for now)

```
$ pip install -U --process-dependency-links okchef
```

Preferably, you've read the install for `requests-chef`, so this will work:

```
# -U ensures you get the latest version
$ pip install -U okchef
```

