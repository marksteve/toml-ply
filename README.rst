========
toml-ply
========

TOML PLY parser. Not a good one but it works (sometimes).
I just wanted to play around with PLY. I had fun so mission complete!

Use
---

.. code-block:: python

    import toml_ply as toml
    with open('config.toml') as f:
        pprint(toml.loads(f.read()), indent=2)

License
-------

http://marksteve.mit-license.org
