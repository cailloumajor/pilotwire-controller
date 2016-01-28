# -*- coding: utf-8 -*-

import os
from setuptools import setup


os.environ['PBR_VERSION'] = '0.3.2'
os.environ['PBR_REQUIREMENTS_FILES'] = 'pbr-requirements.txt'

setup(
    setup_requires=['pbr'],
    pbr=True,
)
