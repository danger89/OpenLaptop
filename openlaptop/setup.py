#!/usr/bin/env python
###############################################################################
#
# file: setup.py
#
# Purpose: installs the OpenLaptop Utility
#
#
###############################################################################
#
# Copyright 2012 Melroy van den Berg
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
###############################################################################
"""
The installation script of OpenLaptop Utility.

sudo python setup.py install --prefix=/usr --install-layout=deb

"""

import os
import platform
from distutils.core import setup

files=[]
for f in os.path.abspath(''):
    files.append(f)

setup(
    name='OpenLaptop',
    version='1.1.1',
    description='OpenLaptop Hulpprogramma.',
    author='Melroy van den Berg',
    author_email='info@openlaptop.nl',
    url='http://www.openlaptop.nl/',
    keywords=['openlaptop', 'hulpprogramma', 'openlaptop hulpprogramma', 'utility'],
    scripts = ['OpenLaptop/openlaptop-hulpprogramma'],       
    data_files=[
        ('/usr/share/openlaptop', ['OpenLaptop/openlaptop-hulpprogramma.ui', 'OpenLaptop/openlaptop-hulpprogramma.png']),
        ('/usr/share/applications', ['OpenLaptop/openlaptop-hulpprogramma.desktop']),
        ('/usr/share/pixmaps', ['OpenLaptop/openlaptop-hulpprogramma.png']),
        ('/usr/share/icons', ['OpenLaptop/openlaptop-hulpprogramma.png']),
        ],
    license='Apache License v2',
    packages = ['OpenLaptop'],
    package_data = {'openlaptop': files},
    classifiers = [
        'Programming Language :: Python',
    ]
)

if __name__ == '__main__':
    #
    # The entry point of this application, as this should not be accessible as
    # a python module to be imported by another application.
    #
    print """
Bedankt dat u gekozen heeft voor OpenLaptop.
"""
