# -*- coding: utf-8 -*-

import os
from setuptools import setup


os.environ['PBR_VERSION'] = '0.6.4'

setup(
    setup_requires=['pbr'],
    pbr=True,
)
