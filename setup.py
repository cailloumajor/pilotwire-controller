# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


setup(
    name='pilotwire-controller',
    version='0.1.0',
    description="Electrical heaters driving controller",
    url='https://github.com/cailloumajor/home-web',
    author="Arnaud Rocher",
    author_email='arnaud.roche3@gmail.com',
    license='GPLv3+',
    packages=find_packages(exclude=['*.tests']),
    test_suite='pilotwire_controller.tests'
)
