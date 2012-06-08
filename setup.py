from setuptools import setup

setup(name='resolv',
      version='1.0.2',
      description='Module for resolving URLs from filehosters, video hosters, and other content hosters',
      author='Sven Slootweg',
      author_email='resolv@cryto.net',
      url='http://cryto.net/resolv',
      packages=['resolv', 'resolv.resolvers'],
      provides=['resolv']
     )
