# -*- coding: utf-8 -*-

import os
from setuptools import setup


os.environ['PBR_VERSION'] = '0.6.7'

setup(
    setup_requires=['pbr'],
    pbr=True,
)
