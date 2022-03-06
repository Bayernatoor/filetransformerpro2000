try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Simple FFMPEG GUI tool',
    'author': 'Bayer',
    'url': '',
    'download_url': '',
    'author_email': '',
    'version': '1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'shapeshifter'
}

setup(**config)
