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

import os
import sys
import datetime

import sublime
from .channel_utilities import clean_urljoin
from .channel_utilities import get_main_directory


# Infer the correct package name and current directory absolute path
CURRENT_DIRECTORY    = os.path.dirname( os.path.realpath( __file__ ) )
CURRENT_PACKAGE_NAME = os.path.basename( CURRENT_DIRECTORY ).rsplit('.', 1)[0]

# Hold all the information for this channel, which will be used by the `ChannelManager` to install
# this channel
g_channel_settings = {}


def plugin_loaded():
    """
        We can only load the information when the Sublime Text API is available due the use of the
        get_main_directory() which requires it.
    """
    global g_channel_settings

    # The folder where the directory where the Sublime Text `Packages` (loose packages) folder is on
    STUDIO_MAIN_DIRECTORY = get_main_directory( CURRENT_DIRECTORY )

    # The folder where the User settings are on
    USER_FOLDER_PATH = os.path.join( STUDIO_MAIN_DIRECTORY, "Packages", "User" )

    # The temporary folder to download the main repository when installing the development version
    g_channel_settings['TEMPORARY_FOLDER_TO_USE'] = "__channel_studio_temp"

    # Where to save the settings for channel after it is installed on the user's machine
    g_channel_settings['USER_FOLDER_PATH']             = USER_FOLDER_PATH
    g_channel_settings['STUDIO_INSTALLATION_SETTINGS'] = os.path.join( USER_FOLDER_PATH, CURRENT_PACKAGE_NAME + ".sublime-settings" )


    # The local path to the files, used to save the generated channels. Valid URLs to the files, to use
    # when installing the stable version of the channel See also:
    # https://packagecontrol.io/docs/channels_and_repositories

    # The default Package Control channel
    g_channel_settings['DEFAULT_CHANNEL_URL'] = "https://packagecontrol.io/channel_v3.json"

    # The URL of the folder where the channel files are hosted
    STUDIO_RAW_URL = "https://raw.githubusercontent.com/evandrocoan/SublimeStudioChannel/master/"

    # The URL to the main A direct URL/Path to the repository where there is the `.gitmodules` file
    # listing all the channel packages to use when generating Studio Channel files.
    g_channel_settings['STUDIO_MAIN_URL']       = "https://github.com/evandrocoan/SublimeTextStudio"
    g_channel_settings['STUDIO_MAIN_DIRECTORY'] = STUDIO_MAIN_DIRECTORY

    # The file path to the Channel File `channel.json` to use when installing the development version
    g_channel_settings['STUDIO_CHANNEL_URL']  = clean_urljoin( STUDIO_RAW_URL, "channel.json" )
    g_channel_settings['STUDIO_CHANNEL_FILE'] = os.path.join( CURRENT_DIRECTORY, "channel.json" )

    # A direct URL/Path to the Repository File `repository.json` to use when installing the stable/development version
    g_channel_settings['STUDIO_REPOSITORY_URL']  = clean_urljoin( STUDIO_RAW_URL, "repository.json" )
    g_channel_settings['STUDIO_REPOSITORY_FILE'] = os.path.join( CURRENT_DIRECTORY, "repository.json" )

    # A direct URL/Path to the `settings.json` to use when installing the stable/development version
    g_channel_settings['STUDIO_SETTINGS_URL']  = clean_urljoin( STUDIO_RAW_URL, "settings.json" )
    g_channel_settings['STUDIO_SETTINGS_PATH'] = os.path.join( CURRENT_DIRECTORY, "settings.json" )


    # The package "BetterFindBuffer" is being installed by after "Default" because it is creating the
    # file "Find Results.hidden-tmLanguage" on the folder "Default" causing the installation of the
    # package "Default" to stop.
    #
    # Some of these packages "SublimeLinter", "SublimeLinter-javac", "A File Icon" need to be installed
    # by last as they were messing with the color scheme settings when installing it on a vanilla
    # install. Todo, fix whatever they are doing and causes the `Preferences.sublime-settings` file to
    # be set to:
    # {
    #     "color_scheme": "Packages/User/SublimeLinter/Monokai (SL).tmTheme"
    # }
    g_channel_settings['PACKAGES_TO_INSTALL_LAST'] = \
    [
        "Default",
        "BetterFindBuffer",
        "SublimeLinter",
        "SublimeLinter-javac",
        "A File Icon"
    ]

    # The default user preferences file
    g_channel_settings['USER_SETTINGS_FILE'] = "Preferences.sublime-settings"

    # Do not try to install this own package and the Package Control, as they are currently running
    g_channel_settings['PACKAGES_TO_NOT_INSTALL'] = [ "Package Control", CURRENT_PACKAGE_NAME ]


    # The files of the default packages you are installed
    g_channel_settings['DEFAULT_PACKAGES_FILES'] = \
    [
        ".gitignore",
        "Context.sublime-menu",
        "Default (Linux).sublime-keymap",
        "Default (Linux).sublime-mousemap",
        "Default (OSX).sublime-keymap",
        "Default (OSX).sublime-mousemap",
        "Default (Windows).sublime-keymap",
        "Default (Windows).sublime-mousemap",
        "Distraction Free.sublime-settings",
        "Find Results.hidden-tmLanguage",
        "Preferences (Linux).sublime-settings",
        "Preferences (OSX).sublime-settings",
        "Preferences (Windows).sublime-settings",
        "Preferences.sublime-settings",
        "README.md",
        "Tab Context.sublime-menu",
        "transpose.py"
    ]


    # Print all their values for debugging
    variables = \
    [
        "%-30s: %s" % ( variable_name, g_channel_settings[variable_name] )
        for variable_name in g_channel_settings.keys()
    ]

    # print("\nImporting %s settings... \n%s" % ( str(datetime.datetime.now())[0:19], "\n".join( sorted(variables) ) ))


