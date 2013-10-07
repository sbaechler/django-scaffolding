#!/usr/bin/env python

from distutils.core import setup
import os
import setuplib

packages, package_data = setuplib.find_packages('scaffolding')

setup(
    name='django-scaffolding',
    version='0.2.2',
    author='Simon Baechler',
    author_email='simon@stellanera.com',
    packages=packages,
    package_data=package_data,
    url='https://github.com/sbaechler/django-scaffolding/',
    license='LICENCE',
    description='Automatically generate reasonable database entries for your app',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
