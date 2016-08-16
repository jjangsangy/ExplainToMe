# -*- coding: utf-8 -*-
"""
Explain To Me
=============
Automatic Web Article Summarizer

:copyright (c) 2015 Sang Han:
"""

from setuptools import setup

from version import __version__ as version

setup(
    name='ExplainToMe',
    description='Automatic Web Article Summarizer',
    long_description='\n'.join(
        [
            open('README.rst', 'rb').read().decode('utf-8'),
            open('HISTORY.rst', 'rb').read().decode('utf-8'),
        ]
    ),
    author='Sang Han',
    license='Apache License 2.0',
    url='https://github.com/jjangsangy/ExplainToMe',
    author_email='jjangsangy@gmail.com',
    include_package_data=True,
    packages=['ExplainToMe'],
    version=version,
    install_requires=['requests', 'sumy'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'explain = ExplainToMe.__main__:main'
        ],
    },
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
