from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='Icarus',
   version='0.1',
   description='A modular personal assistant',
   license="GPGv3",
   long_description=long_description,
   author='derilion',
   author_email='foo@mail.com',
   url="http://www.github.com/derilion/icarus/",
   packages=['src'],
   install_requires=['bar', 'greek'],  # todo: need to be updated to actual dependencies
   scripts=[
            'logger.py',
            'main.py',
           ]
)