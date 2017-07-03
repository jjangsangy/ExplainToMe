# -*- coding: utf-8 -*-
"""
Explain To Me
=============
Automatic Web Article Summarizer

:copyright (c) 2015 Sang Han:
"""

from setuptools import setup

from pkg_resources import resource_filename, resource_exists

def load_version(*filepath):
    assert resource_exists(*filepath)
    namespace = {}
    with open(resource_filename(*filepath)) as f:
        exec(compile(f.read(), filepath[-1], 'exec'), namespace)
    return namespace

setup(
    name='ExplainToMe',
    description='Automatic Web Article Summarizer',
    long_description='\n'.join(
        [
            open('README.md', 'rb').read().decode('utf-8'),
        ]
    ),
    author='Sang Han',
    license='Apache License 2.0',
    url='https://github.com/jjangsangy/ExplainToMe',
    author_email='jjangsangy@gmail.com',
    include_package_data=True,
    packages=['ExplainToMe'],
    version=load_version('ExplainToMe', 'version.py'),
    install_requires=['requests', 'sumy'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Unix Shell',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
    ],
)
