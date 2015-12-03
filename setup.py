from setuptools import setup, find_packages

requires = [
    'clld>=1.7.1',
    'clldmpg>=1.0.0',
    'BeautifulSoup4',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'mock==1.0',
]

setup(name='wals3',
      version='0.0',
      description='wals3',
      long_description='',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='wals3',
      install_requires=requires,
      tests_require=tests_require,
      entry_points="""\
      [paste.app_factory]
      main = wals3:main
      [console_scripts]
      initialize_wals3_db = wals3.scripts.initializedb:main
      """,
      )
