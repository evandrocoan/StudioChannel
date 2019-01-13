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
import threading


g_channelSettings          = {}
g_installation_details     = {}
g_is_settings_load_delayed = False

# How to import python class file from same directory?
# https://stackoverflow.com/questions/21139364/how-to-import-python-class-file-from-same-directory
#
# Global variable is not updating in python
# https://stackoverflow.com/questions/30392157/global-variable-is-not-updating-in-python
from . import settings as g_settings

from channel_manager import channel_installer
from channel_manager import installation_wizard
from channel_manager import uninstallation_wizard

from channel_manager import channel_manager
from channel_manager import submodules_manager
from channel_manager import copy_default_package

from channel_manager.channel_utilities import load_data_file
from channel_manager.channel_utilities import write_data_file
from channel_manager.channel_utilities import get_installed_packages
from channel_manager.channel_utilities import look_for_invalid_default_ignored_packages
from channel_manager.channel_utilities import look_for_invalid_packages


# # Run unit tests
# from channel_manager import channel_manager_tests
# channel_manager_tests.main()

# # How to reload a Sublime Text dependency?
# # https://github.com/randy3k/AutomaticPackageReloader/issues/12
# sublime_plugin.reload_plugin( "channel_manager.channel_installer" )
# sublime_plugin.reload_plugin( "channel_manager.channel_utilities" )
# sublime_plugin.reload_plugin( "channel_manager.channel_manager" )
# sublime_plugin.reload_plugin( "channel_manager.channel_manager_tests" )



from debug_tools import getLogger

# Debugger settings: 0 - disabled, 127 - enabled
log = getLogger( 1, g_settings.CURRENT_PACKAGE_NAME + "." + os.path.basename( __file__ ).split(".")[0] )

log( 2, "..." )
log( 2, "..." )
log( 2, "Debugging" )
log( 2, "PACKAGE_ROOT_DIRECTORY: " + g_settings.PACKAGE_ROOT_DIRECTORY )


class DevelopmentVersionBaseCommand(sublime_plugin.ApplicationCommand):

    def is_enabled(self):
        return is_channel_installed() and is_development_version()


class StudioChannelExtractDefaultPackages(DevelopmentVersionBaseCommand):

    def run(self):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        copy_default_package.main( True )


class StudioChannelRun(DevelopmentVersionBaseCommand):

    def run(self, command):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        submodules_manager.main( command )


class StudioChannelGenerateChannelFile(DevelopmentVersionBaseCommand):

    def run(self, command="all"):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        channel_manager.main( g_channelSettings, command )


class StudioChannelRunChannelAndSubmodules(DevelopmentVersionBaseCommand):

    def run(self, command):
        sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
        channel_manager.main( g_channelSettings, command )
        submodules_manager.main( command )


class StudioChannelRunInstallation(sublime_plugin.ApplicationCommand):

    def run(self):
        installation_wizard.main( g_channelSettings )

    def is_enabled(self):
        return not is_channel_installed()


class StudioChannelRunUninstallation(sublime_plugin.ApplicationCommand):

    def run(self):
        """
            You can always run the uninstaller, either to uninstall everything, or just this
            package or just some packages.
        """
        uninstallation_wizard.main( g_channelSettings )


def plugin_loaded():
    threading.Thread(target=run_setup_operations).start()


def run_setup_operations():
    installed_packages = get_installed_packages( list_default_packages=True, list_dependencies=True )
    look_for_invalid_default_ignored_packages( installed_packages )

    if load_channel_settings():
        load_installation_details()
        run_channel_update( installed_packages )


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
    if hasattr( g_settings, "g_channelSettings" ) \
            and "CHANNEL_INSTALLATION_DETAILS" in g_settings.g_channelSettings:

        global g_channelSettings
        g_channelSettings = g_settings.g_channelSettings

    else:
        global g_is_settings_load_delayed

        # Stop delaying indefinitely
        if g_is_settings_load_delayed:
            log.newline()
            log( 1, "Error: Could not load the settings files! g_channelSettings: " + str( g_channelSettings ) )

        else:
            g_is_settings_load_delayed = True
            sublime.set_timeout( plugin_loaded, 2000 )

        return False

    return True


def run_channel_update(installed_packages):
    """
        Call the channel upgrade/downgrade wizards to maintain old installation up to date with the
        main channel file when there are new packages additions or deletions.
    """

    if is_channel_installed():
        g_channelSettings['INSTALLATION_TYPE'] = "upgrade"

        if is_development_version():
            look_for_invalid_packages( g_channelSettings, installed_packages )

        copy_default_package.main( False )
        channel_installer.main( g_channelSettings )

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
    return g_installation_details.get( "automatically_show_installation_wizard", False )


def is_development_version():
    """
        We can only run this when we are using the stable version of the channel. And when there is
        not a `.git` folder, we are running the `Development Version` of the channel.
    """
    return g_installation_details.get( "installation_type", "" ) == "development"


def is_channel_installed():
    """
        Returns True if the channel is installed, i.e., there are packages added to the
        `packages_to_uninstall` list.
    """
    has_installed_packages = len( g_installation_details.get( "packages_to_uninstall", [] ) ) > 0
    return has_installed_packages


def get_channel_file_setting(settings_name, default_value):
    """
        The same as `is_channel_installed`, but allows you to query any third party setting which
        can be set on the user personal channel settings file.

        @param `settings_name` the name of the setting on the file
        @param `default_value` the value to be returned, in case the setting does not exists on the user file
    """
    custom_user_setting = g_installation_details.get( settings_name, default_value )
    return custom_user_setting

