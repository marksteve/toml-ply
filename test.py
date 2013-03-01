from pprint import pprint

import toml_ply as toml


for test_file in ('example.toml', 'hard_example.toml', 'numbers.toml'):
    with open('tests/' + test_file) as f:
        pprint(toml.loads(f.read()), indent=2)

