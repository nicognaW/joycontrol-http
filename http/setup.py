from setuptools import setup, find_packages

setup(name='joycontrol-http',
      version='0.14',
      author='Nico Gnaw',
      author_email='nicognaw@outlook.com',
      description='Build HTTP api for joycontrol.',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'hid', 'aioconsole', 'dbus-python', 'crc8', 'fastapi', 'uvicorn'
      ])
