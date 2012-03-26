from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-scaffolding',
    version='0.1.0',
    author='Simon Baechler',
    author_email='simon@stellanera.com',
    packages=find_packages(),
    url='https://github.com/sbaechler/django-scaffolding',
    license='LICENSE',
    description='Automatically generate reasonable database entries for your app',
    long_description=open('README.rst').read(),
    install_requires=[
        "Django >= 1.2",
    ],
    zip_safe=False
)