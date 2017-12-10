#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# These lines allow to use UTF-8 encoding and run this file with `./update.py`, instead of `python update.py`
# https://stackoverflow.com/questions/7670303/purpose-of-usr-bin-python3
# https://stackoverflow.com/questions/728891/correct-way-to-define-python-source-code-encoding
#
#

#
# Licensing
#
# Studio Channel Commands, create commands for the Channel Manager
# Copyright (C) 2017 Evandro Coan <https://github.com/evandrocoan>
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

import sublime
import sublime_plugin

import os


# How to import python class file from same directory?
# https://stackoverflow.com/questions/21139364/how-to-import-python-class-file-from-same-directory
#
# Global variable is not updating in python
# https://stackoverflow.com/questions/30392157/global-variable-is-not-updating-in-python
from . import settings
from . import installation_wizard

from . import installation_wizard
from . import uninstallation_wizard

from channel_manager import channel_manager
from channel_manager import submodules_manager
from channel_manager import copy_default_package

# How to reload a Sublime Text dependency?
# https://github.com/randy3k/AutomaticPackageReloader/issues/12
sublime_plugin.reload_plugin( "channel_manager.channel_manager" )


# If a dependency fail running, the subsequent dependencies are not installed by Package Control
# https://github.com/wbond/package_control/issues/1301
try:
    from python_debug_tools import Debugger

    # Debugger settings: 0 - disabled, 127 - enabled
    log = Debugger( 1, os.path.basename( __file__ ) )

    log( 2, "..." )
    log( 2, "..." )
    log( 2, "Debugging" )
    log( 2, "CURRENT_DIRECTORY: " + settings.CURRENT_DIRECTORY )

except Exception as error:
    print( "Could not import the required dependencies! " + str( error ) )


class StudioChannelRunUninstallationWizard( sublime_plugin.ApplicationCommand ):

    def run(self):
        installation_wizard.main()


class StudioChannelRunInstallationWizard( sublime_plugin.ApplicationCommand ):

    def run(self):
        installation_wizard.main()

    def is_enabled(self):
        return installation_wizard.g_is_package_control_installed


class StudioChannelGenerateChannelFile( sublime_plugin.ApplicationCommand ):

    def run(self, command="all"):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        channel_manager.main( settings.g_channel_settings, command )

    def is_enabled(self):
        return not installation_wizard.g_is_package_control_installed


class StudioChannelRun( sublime_plugin.ApplicationCommand ):

    def run(self, run):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        submodules_manager.main( run )

    def is_enabled(self):
        return not installation_wizard.g_is_package_control_installed


class StudioChannelExtractDefaultPackages( sublime_plugin.ApplicationCommand ):

    def run(self):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        copy_default_package.main( settings.g_channel_settings['DEFAULT_PACKAGES_FILES'], True )

    def is_enabled(self):
        return not installation_wizard.g_is_package_control_installed


is_delayed = False

def plugin_loaded():

    # the settings are not yet loaded, wait a little
    if "DEFAULT_PACKAGES_FILES" not in settings.g_channel_settings:
        global is_delayed

        # Stop delaying indefinitely
        if is_delayed:
            log( 1, "Error: Could not load the settings files! g_channel_settings:" + str( settings.g_channel_settings ) )
            return

        is_delayed = True
        sublime.set_timeout( plugin_loaded, 2000 )

    else:
        is_forced = False
        # is_forced = True

        copy_default_package.main( settings.g_channel_settings['DEFAULT_PACKAGES_FILES'], is_forced )


