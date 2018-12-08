#! /usr/bin/env python
# -*- coding: utf-8 -*-

####################### Licensing #######################################################
#
#   Copyright 2018 @ Evandro Coan
#   Project Unit Tests
#
#  Redistributions of source code must retain the above
#  copyright notice, this list of conditions and the
#  following disclaimer.
#
#  Redistributions in binary form must reproduce the above
#  copyright notice, this list of conditions and the following
#  disclaimer in the documentation and/or other materials
#  provided with the distribution.
#
#  Neither the name Evandro Coan nor the names of any
#  contributors may be used to endorse or promote products
#  derived from this software without specific prior written
#  permission.
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or ( at
#  your option ) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################################
#

import os
import sys

import unittest
import sublime_plugin

from debug_tools import testing_utilities

from channel_manager import channel_installer
from channel_manager import installation_wizard

from StudioChannel import commands
from StudioChannel import settings


# from channelmanager import studio_installer; studio_installer.main("development")
# from channelmanager import studio_installer; studio_installer.main("stable")
# from channelmanager import studio_uninstaller; studio_uninstaller.main()
# from StudioChannel import installation_wizard; installation_wizard.install()
class MainUnitTests(testing_utilities.TestingUtilities):

    def setUp(self):
        commands.load_channel_settings()
        commands.load_installation_details()
        is_channel_installed = commands.is_channel_installed()

        if commands.is_channel_installed():
            self.fail("You cannot run the installation test when the channel is already installed! (%s)" % is_channel_installed)

    def test_installationAndUninstallationStable(self):
        installation_wizard.unpack_settigns(settings.g_channelSettings)
        installation_wizard.add_channel()
        installation_wizard.clear_cache()

        installation_wizard.g_channelSettings['INSTALLER_TYPE']    = "installer"
        installation_wizard.g_channelSettings['INSTALLATION_TYPE'] = "stable"
        installation_wizard.g_channelSettings['SKIP_INSTALLATION_QUESTIONS'] = "Useful for Automated Unit Testing"

        installer_thread = channel_installer.main( installation_wizard.g_channelSettings, True )
        installer_thread.join()

        self.fail("Not yet implemented")

    def test_installationAndUninstallationDevelopment(self):
        pass

    def test_upgradeStable(self):
        pass

    def test_upgradeDevelopment(self):
        pass

    def test_downgradeStable(self):
        pass

    def test_downgradeDevelopment(self):
        pass

