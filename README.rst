========
toml-ply
========

TOML PLY parser. Still missing some restrictions and error handling but mostly works :)


Supports (supposedly)
-------
https://github.com/mojombo/toml/commit/3f4224ecdc4a65fdd28b4fb70d46f4c0bd3700aa


Use
---

.. code-block:: python

    import toml_ply as toml
    with open('config.toml') as f:
        pprint(toml.loads(f.read()), indent=2)


License
-------

http://marksteve.mit-license.org
