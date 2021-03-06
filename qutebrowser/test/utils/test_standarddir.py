# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2014-2015 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for qutebrowser.utils.standarddir."""

import os
import os.path
import sys
import shutil
import unittest
import tempfile

from qutebrowser.utils import standarddir
from qutebrowser.test import helpers, qApp


class GetStandardDirLinuxTests(unittest.TestCase):

    """Tests for standarddir under Linux.

    Attributes:
        temp_dir: A temporary directory.
        old_name: The old applicationName.
    """

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.old_name = qApp.applicationName()
        qApp.setApplicationName('qutebrowser')

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux")
    def test_data_explicit(self):
        """Test data dir with XDG_DATA_HOME explicitely set."""
        with helpers.environ_set_temp({'XDG_DATA_HOME': self.temp_dir}):
            standarddir.init(None)
            expected = os.path.join(self.temp_dir, 'qutebrowser')
            self.assertEqual(standarddir.data(), expected)

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux")
    def test_config_explicit(self):
        """Test config dir with XDG_CONFIG_HOME explicitely set."""
        with helpers.environ_set_temp({'XDG_CONFIG_HOME': self.temp_dir}):
            standarddir.init(None)
            expected = os.path.join(self.temp_dir, 'qutebrowser')
            self.assertEqual(standarddir.config(), expected)

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux")
    def test_cache_explicit(self):
        """Test cache dir with XDG_CACHE_HOME explicitely set."""
        with helpers.environ_set_temp({'XDG_CACHE_HOME': self.temp_dir}):
            standarddir.init(None)
            expected = os.path.join(self.temp_dir, 'qutebrowser')
            self.assertEqual(standarddir.cache(), expected)

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux")
    def test_data(self):
        """Test data dir with XDG_DATA_HOME not set."""
        env = {'HOME': self.temp_dir, 'XDG_DATA_HOME': None}
        with helpers.environ_set_temp(env):
            standarddir.init(None)
            expected = os.path.join(self.temp_dir, '.local', 'share',
                                    'qutebrowser')
            self.assertEqual(standarddir.data(), expected)

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux")
    def test_config(self):
        """Test config dir with XDG_CONFIG_HOME not set."""
        env = {'HOME': self.temp_dir, 'XDG_CONFIG_HOME': None}
        with helpers.environ_set_temp(env):
            standarddir.init(None)
            expected = os.path.join(self.temp_dir, '.config', 'qutebrowser')
            self.assertEqual(standarddir.config(), expected)

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux")
    def test_cache(self):
        """Test cache dir with XDG_CACHE_HOME not set."""
        env = {'HOME': self.temp_dir, 'XDG_CACHE_HOME': None}
        with helpers.environ_set_temp(env):
            standarddir.init(None)
            expected = os.path.join(self.temp_dir, '.cache', 'qutebrowser')
            self.assertEqual(standarddir.cache(), expected)

    def tearDown(self):
        qApp.setApplicationName(self.old_name)
        shutil.rmtree(self.temp_dir)


class GetStandardDirWindowsTests(unittest.TestCase):

    """Tests for standarddir under Windows.

    Attributes:
        old_name: The old applicationName.
    """

    def setUp(self):
        self.old_name = qApp.applicationName()
        # We can't store the files in a temp dir, so we don't chose qutebrowser
        qApp.setApplicationName('qutebrowser_test')
        standarddir.init(None)

    def tearDown(self):
        qApp.setApplicationName(self.old_name)

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_data(self):
        """Test data dir."""
        self.assertEqual(standarddir.data().split(os.sep)[-2:],
                         ['qutebrowser_test', 'data'], standarddir.data())

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_config(self):
        """Test config dir."""
        self.assertEqual(standarddir.config().split(os.sep)[-1],
                         'qutebrowser_test',
                         standarddir.config())

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_cache(self):
        """Test cache dir."""
        self.assertEqual(standarddir.cache().split(os.sep)[-2:],
                         ['qutebrowser_test', 'cache'], standarddir.cache())
