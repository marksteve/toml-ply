from setuptools import setup

if __name__ == '__main__':
    setup(name='toml-ply',
          version='0.0.3',
          description="TOML PLY parser",
          author="Mark Steve Samson",
          author_email="hello@marksteve.com",
          url='https://github.com/marksteve/toml-ply',
          license='MIT',
          py_modules=['toml_ply'],
          install_requires=['ply'],
          )
