from distutils.core import setup

setup(
    windows=['__init__.py'],
    options={
        "py2exe": {
            "unbuffered": True,
            "optimize": 2,
            "packages": "resources"
        }
    }
)
