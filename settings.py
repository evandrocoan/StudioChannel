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
from .channel_utilities import get_main_directory


# Hold all the information for this channel, which will be used by the `ChannelManager` to install
# this channel
g_channel_settings = {}

# Infer the correct package name and current directory absolute path
CURRENT_DIRECTORY    = os.path.dirname( os.path.realpath( __file__ ) )
CURRENT_PACKAGE_NAME = os.path.basename( CURRENT_DIRECTORY ).rsplit('.', 1)[0]

# The folder where the studio channel will be installed
STUDIO_MAIN_DIRECTORY = get_main_directory( CURRENT_DIRECTORY )

# Where to save the settings for channel after it is installed on the user's machine
g_channel_settings['channel_settings'] = os.path.join( STUDIO_MAIN_DIRECTORY, "Packages", "User", CURRENT_PACKAGE_NAME + ".sublime-settings" )


# The temporary folder to download the main repository when installing the development version
g_channel_settings['temporary_folder_to_use'] = "__channel_studio_temp"

# The URL to the main repository where there is the `.gitmodules` files listing all the channel packages
g_channel_settings['studio_main_url'] = "https://github.com/evandrocoan/SublimeTextStudio"

# The directory where the Sublime Text `Packages` (loose packages) folder is on
g_channel_settings['studio_main_directory'] = STUDIO_MAIN_DIRECTORY

# A direct URL to the Channel File `settings.json` to use when installing the stable version
g_channel_settings['channel_main_file_url']  = "https://raw.githubusercontent.com/evandrocoan/SublimeStudioChannel/master/settings.json"

# The file path to the Channel File `settings.json` to use when installing the development version
g_channel_settings['channel_main_file_path'] = os.path.join( STUDIO_MAIN_DIRECTORY, "Packages", "StudioChannel", "settings.json" )


# The local path to the files, to use when installing the development version of the channel
# See also: https://packagecontrol.io/docs/channels_and_repositories
g_channel_settings['studio_channel_file']    = os.path.join( CURRENT_DIRECTORY, "channel.json" )
g_channel_settings['studio_repository_file'] = os.path.join( CURRENT_DIRECTORY, "repository.json" )
g_channel_settings['studio_setttings_file']  = os.path.join( CURRENT_DIRECTORY, "settings.json" )

# Valid URLs to the files, to use when installing the stable version of the channel
g_channel_settings['default_channel_url'] = "https://packagecontrol.io/channel_v3.json"
g_channel_settings['channel_file_url']    = "https://raw.githubusercontent.com/evandrocoan/SublimeStudioChannel/master/repository.json"


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
g_channel_settings['packages_to_install_last'] = ["Default", "BetterFindBuffer", "SublimeLinter", "SublimeLinter-javac", "A File Icon"]

# Do not try to install this own package and the Package Control, as they are currently running
g_channel_settings['packages_to_not_install'] = [ "Package Control", CURRENT_PACKAGE_NAME ]

# The default user preferences file
g_channel_settings['user_settings_file'] = "Preferences.sublime-settings"


# The files of the default packages you are installed
g_channel_settings['default_packages_files'] = \
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


