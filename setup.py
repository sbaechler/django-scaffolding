#!/usr/bin/env python

from setuptools import setup, find_packages
import os


setup(
    name='django-scaffolding',
    version='0.2.6',
    author='Simon Baechler',
    author_email='simon@stellanera.com',
    packages=find_packages(
        exclude=['tests', 'example']
    ),
    package_data={
        '': ['*.html', '*.txt'],
        'scaffolding': [
            'library/*.csv'
        ]
    },
    url='https://github.com/sbaechler/django-scaffolding/',
    license='MIT',
    description='Automatically generate reasonable database entries for your app',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    zip_safe=False
)
