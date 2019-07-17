from distutils.core import setup
from setuptools import find_packages

setup(
    name='isharp',
    packages=find_packages(),
    version='1.8',
    description='Algorithmic workbench',
    author='jeremycward',
    author_email='jeremycward@yahoo.co.uk',
    url='https://github.com/jeremycward/isharp-core',
    download_url='https://github.com/jeremycward/isharp-core/tarball/1.00',
    keywords=['string', 'reverse'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'datahub=isharp.broker_service.datahub_main:main',
        ]
    },
)
