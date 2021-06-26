from setuptools import setup

setup(
    name='crawllib',
    version='0.0.1',
    author='Nico Hoffmann',
    author_email='n-py-crawllib@maxdoom.com',
    packages=['crawllib',],
    url='https://github.com/maxdoom-com/crawllib/',
    license='LICENSE.md',
    description='A tiny crawling library',
    long_description=open('README.md').read(),
    install_requires=[
        'requests',
        'unidecode',
        'lxml',
        'cssselect',
        'urllib',
    ],
)
