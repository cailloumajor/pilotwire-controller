# -*- coding: utf-8 -*-

import os
from setuptools import setup


os.environ['PBR_VERSION'] = '0.3.3'

setup(
    setup_requires=['pbr'],
    pbr=True,
)
