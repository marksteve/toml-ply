from pprint import pprint

import toml_ply as toml


with open('example.toml') as f:
    pprint(toml.loads(f.read()), indent=2)
