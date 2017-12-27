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


g_channelSettings          = {}
g_installation_details     = {}
g_is_settings_load_delayed = False

# How to import python class file from same directory?
# https://stackoverflow.com/questions/21139364/how-to-import-python-class-file-from-same-directory
#
# Global variable is not updating in python
# https://stackoverflow.com/questions/30392157/global-variable-is-not-updating-in-python
from . import settings

from channel_manager import installation_wizard
from channel_manager import uninstallation_wizard

from channel_manager import channel_installer
from channel_manager import channel_uninstaller

from channel_manager import channel_manager
from channel_manager import submodules_manager
from channel_manager import copy_default_package

from channel_manager.channel_utilities import clean_urljoin
from channel_manager.channel_utilities import load_data_file
from channel_manager.channel_utilities import get_main_directory
from channel_manager.channel_utilities import get_dictionary_key
from channel_manager.channel_utilities import write_data_file

# # Run unit tests
# from channel_manager import channel_manager_tests
# channel_manager_tests.main()

# # How to reload a Sublime Text dependency?
# # https://github.com/randy3k/AutomaticPackageReloader/issues/12
# sublime_plugin.reload_plugin( "channel_manager.channel_utilities" )
# sublime_plugin.reload_plugin( "channel_manager.channel_manager" )
# sublime_plugin.reload_plugin( "channel_manager.channel_manager_tests" )

# sublime_plugin.reload_plugin( "channel_manager.channel_installer" )
# sublime_plugin.reload_plugin( "channel_manager.channel_uninstaller" )


from python_debug_tools import Debugger

# Debugger settings: 0 - disabled, 127 - enabled
log = Debugger( 1, settings.CURRENT_PACKAGE_NAME + ", " + os.path.basename( __file__ ) )

log( 2, "..." )
log( 2, "..." )
log( 2, "Debugging" )
log( 2, "CURRENT_PACKAGE_ROOT_DIRECTORY: " + settings.CURRENT_PACKAGE_ROOT_DIRECTORY )


class StudioChannelExtractDefaultPackages( sublime_plugin.ApplicationCommand ):

    def run(self):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        copy_default_package.main( g_channelSettings['DEFAULT_PACKAGE_FILES'], True )

    def is_enabled(self):
        return is_channel_installed() and is_development_version()


class StudioChannelRun( sublime_plugin.ApplicationCommand ):

    def run(self, run):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        submodules_manager.main( run )

    def is_enabled(self):
        return is_channel_installed() and is_development_version()


class StudioChannelGenerateChannelFile( sublime_plugin.ApplicationCommand ):

    def run(self, command="all"):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        channel_manager.main( g_channelSettings, command )

    def is_enabled(self):
        return is_channel_installed() and is_development_version()


class StudioChannelRunInstallation( sublime_plugin.ApplicationCommand ):

    def run(self):
        installation_wizard.main( g_channelSettings )

    def is_enabled(self):
        return not is_channel_installed()


class StudioChannelRunUninstallation( sublime_plugin.ApplicationCommand ):

    def run(self):
        """
            You can always run the uninstaller, either to uninstall everything, or just this
            package or just some packages.
        """
        uninstallation_wizard.main( g_channelSettings )


def plugin_loaded():

    if load_channel_settings():
        load_installation_details()
        run_channel_update()


def load_installation_details():

    # Only attempt to check it, if the settings are loaded
    if len( g_channelSettings ) > 0:
        installationDetailsPath = g_channelSettings['CHANNEL_INSTALLATION_DETAILS']

        if not os.path.exists( installationDetailsPath ):
            write_data_file( installationDetailsPath, {"automatically_show_installation_wizard": True} )

        global g_installation_details
        g_installation_details = load_data_file( installationDetailsPath )


def load_channel_settings():

    # If the settings are not yet loaded, wait a little
    if hasattr( settings, "g_channelSettings" ) \
            and "DEFAULT_PACKAGE_FILES" in settings.g_channelSettings:

        global g_channelSettings
        g_channelSettings = settings.g_channelSettings

    else:
        global g_is_settings_load_delayed

        # Stop delaying indefinitely
        if g_is_settings_load_delayed:
            log.insert_empty_line()
            log( 1, "Error: Could not load the settings files! g_channelSettings: " + str( g_channelSettings ) )

        else:
            g_is_settings_load_delayed = True
            sublime.set_timeout( plugin_loaded, 2000 )

        return False

    return True


def run_channel_update():
    """
        Call the channel upgrade/downgrade wizards to maintain old installation up to date with the
        main channel file when there are new packages additions or deletions.
    """

    if is_channel_installed():
        g_channelSettings['INSTALLATION_TYPE'] = ""
        copy_default_package.main( g_channelSettings['DEFAULT_PACKAGE_FILES'], False )

        g_channelSettings['INSTALLATION_TYPE'] = "upgrade"
        channel_installer.main( g_channelSettings )

        g_channelSettings['INSTALLATION_TYPE'] = "downgrade"
        channel_uninstaller.main( g_channelSettings )

        # Restore the default value
        g_channelSettings['INSTALLATION_TYPE'] = ""

    else:
        sublime.set_timeout_async( check_for_the_first_time, 1000 )


def check_for_the_first_time():
    """
        Automatically run the channel installer wizard when installing the channel package for the
        first time.
    """
    if is_the_first_load_time():
        installation_wizard.main( g_channelSettings )


def is_the_first_load_time():
    """
        Check whether this is the first time the user is running it. If so, then start the
        installation wizard to install the channel or postpone the installation process.

        If the installation is postponed, then the user must to manually start it by running its
        command on the command palette or in the preferences menu.
    """
    channelSettingsPath = g_channelSettings['CHANNEL_INSTALLATION_DETAILS']
    return get_dictionary_key( g_installation_details, "automatically_show_installation_wizard", False )


def is_development_version():
    """
        We can only run this when we are using the stable version of the channel. And when there is
        not a `.git` folder, we are running the `Development Version` of the channel.
    """
    return get_dictionary_key( g_installation_details, "installation_type", "" ) == "development"


def is_channel_installed():
    """
        Returns True if the channel is installed, i.e., there are packages added to the
        `packages_to_uninstall` list.
    """
    return len( get_dictionary_key( g_installation_details, "packages_to_uninstall", [] ) ) > 0

