import json

import toml_ply as toml


data = '''server = 128
[config]
a = 3
b = 2
[config.defaults]
c = 2
'''

print json.dumps(toml.loads(data), indent=2)
