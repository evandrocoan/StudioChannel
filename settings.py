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

import os
import sys
import datetime


# The temporary folder to download the main repository when installing the development version
TEMPORARY_FOLDER_TO_USE = "__channel_studio_temp"

# Infer the correct package name and current directory absolute path
CURRENT_DIRECTORY    = os.path.dirname( os.path.realpath( __file__ ) )
CURRENT_PACKAGE_NAME = os.path.basename( CURRENT_DIRECTORY ).rsplit('.', 1)[0]

# The URL to the main repository where there is the `.gitmodules` files listing all the channel
# packages
STUDIO_MAIN_URL = "https://github.com/evandrocoan/SublimeTextStudio"

# The directory where the Sublime Text `Packages` (loose packages) folder is on
STUDIO_MAIN_DIRECTORY = os.path.dirname( sublime.packages_path() )

# A direct URL to the Channel File `settings.json` to use when installing the stable version
CHANNEL_MAIN_FILE_URL  = "https://raw.githubusercontent.com/evandrocoan/SublimeStudioChannel/master/settings.json"

# The file path to the Channel File `settings.json` to use when installing the development version
CHANNEL_MAIN_FILE_PATH = os.path.join( STUDIO_MAIN_DIRECTORY, "Packages", "StudioChannel", "settings.json" )


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
PACKAGES_TO_INSTALL_LAST = ["Default", "BetterFindBuffer", "SublimeLinter", "SublimeLinter-javac", "A File Icon"]

# Do not try to install this own package and the Package Control, as they are currently running
PACKAGES_TO_NOT_INSTALL = [ "Package Control", CURRENT_PACKAGE_NAME ]

# The default user preferences file
USER_SETTINGS_FILE = "Preferences.sublime-settings"

# The files of the default packages you are installed
DEFAULT_PACKAGES_FILES = \
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
variables = [ "%-30s: %s" % ( variable_name, globals()[variable_name] )
        for variable_name in globals().keys() if variable_name in globals() and isinstance( globals()[variable_name], str ) ]

# print("\nImporting %s settings... \n%s" % ( str(datetime.datetime.now())[0:19], "\n".join(sorted(variables)) ))


