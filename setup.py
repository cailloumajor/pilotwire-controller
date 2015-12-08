# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


setup(
    name='pilotwire-controller',
    version='0.2.2',
    description="Electrical heaters driving controller",
    url='https://github.com/cailloumajor/home-web',
    author="Arnaud Rocher",
    author_email='arnaud.roche3@gmail.com',
    license='GPLv3+',
    packages=find_packages(exclude=['*.tests']),
    test_suite='pilotwire_controller.tests',
    tests_require=['pifacedigitalio', 'pifacecommon'],
    install_requires=['stevedore'],
    extras_require={
        'PiFaceDigital': ['pifacedigitalio', 'pifacecommon'],
    },
    entry_points={
        'console_scripts': [
            "pwcontrollerd = pilotwire_controller.server:main",
        ],
        'pilotwire.controller': [
            ("piface = pilotwire_controller.controller.piface:PiFaceController "
             "[PiFaceDigital]"),
            "test = pilotwire_controller.tests.utils:TestingController",
        ],
    },
)
