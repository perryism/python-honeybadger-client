from distutils.core import setup

with open('requirements.txt') as file:
    install_requires = file.readlines()

setup(name='honeybadger-client',
      version='0.1',
      py_modules=['honeybadger'],
      install_requires=install_requires,
      )
