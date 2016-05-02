import sys
from setuptools import setup, find_packages


assert sys.version_info >= (3, 5), "Python 3.5+ is required!"


requires = [
    'sqlalchemy>=1.0.0',
    'aiohttp',
    'aiohttp_themes',
    'aiohttp_debugtoolbar',
    'coloredlogs',
]


setup(name='aiohttp_chat',
      version='0.0.1.dev',
      description='aiohttp_chat',
      long_description='',
      # Using this invalid trove classifier prevents accidentally uploading
      # something to pypi.
      classifiers=['Private :: Do Not Upload'],
      author='Scott Torborg',
      author_email='storborg@gmail.com',
      license='MIT',
        url='https://github.com/storborg/aiohttp_chat',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='aiohttp_chat',
      install_requires=requires,
      entry_points="""\
      [console_scripts]
      aiohttp_chat_server = aiohttp_chat.server:main
      """,
      )
