import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-rest-encrypted-lookup',
    version='0.1',
    packages=['rest_framework_model_field_permissions'],
    include_package_data=True,
    license='GNU General Public License v3 (GPLv3)',
    description='By model-field permissions for Django Rest Framework.',
    long_description=README,
    url='https://intersis.org/',
    author='The Intersis Foundation',
    author_email='dev@intersis.org',
    install_requires=[
        'django>=1.7',
        'djangorestframework>=3.0.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
