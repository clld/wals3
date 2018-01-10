from setuptools import setup, find_packages

setup(
    name='wals3',
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
    install_requires=[
        'clldutils~=2.0',
        'clld~=4.0',
        'clldmpg~=3.0.0',
        'BeautifulSoup4',
    ],
    extras_require={
        'dev': ['flake8', 'waitress', 'psycopg2'],
        'test': [
            'tox',
            'mock',
            'pytest>=3.1',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    entry_points="""\
[paste.app_factory]
main = wals3:main
[console_scripts]
initialize_wals3_db = wals3.scripts.initializedb:main
""")
