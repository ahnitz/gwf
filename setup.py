# Copyright (C) 2016 Alex Nitz
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
setup.py file for gwf package
"""
try:
    from setuptools import setup
except:
    from distutils.core import setup
 
install_requires =  ['numpy']
version = '0.1.dev0'

setup (
    name = 'gwf',
    version = version,
    description = 'Read gravitational-wave frame files',
    author = 'Alex Nitz',
    author_email = 'alex.nitz@ligo.org',
    url = 'https://github.com/ahnitz/gwf',
    download_url = 'https://github.com/ahnitz/gwf/tarball/v%s' % version,
    keywords = ['ligo', 'physics', 'gravity', 'signal processing'],
    install_requires = install_requires,
    packages = [
               'gwf',
               ],
)
