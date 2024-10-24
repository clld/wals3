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
        'tqdm',
        'clld>=11.3.1',
        'clldutils>=3.6',
        'clldmpg>=4.0.0',
        'csvw>=1.8.1',
        'BeautifulSoup4>=4.9.1',
        'html5lib>=1.1',
        'sqlalchemy>=1.3.20',
        'waitress'
    ],
    extras_require={
        'dev': [
            'flake8',
            'tox',
        ],
        'test': [
            'mock>=4.0.2',
            'psycopg2-binary',
            'pytest>=6.2.1',
            'pytest-clld>=1.0.2',
            'pytest-mock>=3.3.1',
            'pytest-cov>=2.10.1',
            'coverage>=5.3',
            'selenium',
            'zope.component>=4.6.2',
        ],
    },
    entry_points={
        'paste.app_factory': [
            'main = wals3:main',
        ],
    },
)
