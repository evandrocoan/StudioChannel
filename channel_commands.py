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

from .installation_wizard import main as wizard_main
from .uninstallation_wizard import main as unwizard_main

from ChannelManager.channel_manager import main as manager_main
from ChannelManager.submodules_manager import main as submodules_main
from ChannelManager.copy_default_package import main as default_main


# Import the debugger
from debug_tools import Debugger

# Debugger settings: 0 - disabled, 127 - enabled
log = Debugger( 1, os.path.basename( __file__ ) )

log( 2, "..." )
log( 2, "..." )
log( 2, "Debugging" )
log( 2, "CURRENT_DIRECTORY: " + settings.CURRENT_DIRECTORY )


class StudioChannelRunInstalltionWizard( sublime_plugin.ApplicationCommand ):

    def run(self):
        wizard_main()

    def is_enabled(self):
        return installation_wizard.g_is_package_control_installed


class StudioChannelRunUninstalltionWizard( sublime_plugin.ApplicationCommand ):

    def run(self):
        unwizard_main()


class StudioChannelGenerateChannelFile( sublime_plugin.ApplicationCommand ):

    def run(self):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        manager_main( settings.g_channel_settings )


class StudioChannelRun( sublime_plugin.ApplicationCommand ):

    def run(self, run):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        submodules_main( run )


class StudioChannelUpdateDefaultPackages( sublime_plugin.ApplicationCommand ):

    def run(self):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        default_main( settings.g_channel_settings['DEFAULT_PACKAGES_FILES'], True )


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

        default_main( settings.g_channel_settings['DEFAULT_PACKAGES_FILES'], is_forced )


