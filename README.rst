========
toml-ply
========

TOML PLY parser. Still missing some restrictions and error handling but mostly works :)

Use
---

.. code-block:: python

    import toml_ply as toml
    with open('config.toml') as f:
        pprint(toml.loads(f.read()), indent=2)

License
-------

http://marksteve.mit-license.org
