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
# Studio Channel Settings, all the settings required by this channel
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

import os
import sys
import datetime

import sublime
from channel_manager.channel_utilities import clean_urljoin
from channel_manager.channel_utilities import get_main_directory


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
    CHANNEL_ROOT_DIRECTORY = get_main_directory( CURRENT_DIRECTORY )

    # The folder where the User settings are on
    USER_FOLDER_PATH = os.path.join( CHANNEL_ROOT_DIRECTORY, "Packages", "User" )

    # The temporary folder to download the main repository when installing the development version
    g_channel_settings['TEMPORARY_FOLDER_TO_USE'] = "__channel_temporary_directory"
    g_channel_settings['CHANNEL_PACKAGE_NAME']    = CURRENT_PACKAGE_NAME

    # Where to save the settings for channel after it is installed on the user's machine
    g_channel_settings['USER_FOLDER_PATH']              = USER_FOLDER_PATH
    g_channel_settings['CHANNEL_INSTALLATION_SETTINGS'] = \
            os.path.join( USER_FOLDER_PATH, CURRENT_PACKAGE_NAME + ".sublime-settings" )


    # The local path to the files, used to save the generated channels and valid URLs to the files,
    # to use when installing the stable version of the channel. See also:
    # https://packagecontrol.io/docs/channels_and_repositories

    # The default Package Control channel
    g_channel_settings['DEFAULT_CHANNEL_URL'] = "https://packagecontrol.io/channel_v3.json"

    # The URL of the directory where the files `channel.json` and `repository.json` are hosted
    CHANNEL_RAW_URL = "https://raw.githubusercontent.com/evandrocoan/SublimeStudioChannel/master/"

    # The URL to the main A direct URL/Path to the repository where there is the `.gitmodules` file
    # listing all the channel packages to use when generating Studio Channel files.
    g_channel_settings['CHANNEL_ROOT_URL']       = "https://github.com/evandrocoan/SublimeTextStudio"
    g_channel_settings['CHANNEL_ROOT_DIRECTORY'] = CHANNEL_ROOT_DIRECTORY

    # The file path to the Channel File `channel.json` to use when installing the development version
    g_channel_settings['CHANNEL_FILE_URL']  = clean_urljoin( CHANNEL_RAW_URL, "channel.json" )
    g_channel_settings['CHANNEL_FILE_PATH'] = os.path.join( CURRENT_DIRECTORY, "channel.json" )

    # A direct URL/Path to the Repository File `repository.json` to use when installing the
    # stable/development version
    g_channel_settings['CHANNEL_REPOSITORY_URL']  = clean_urljoin( CHANNEL_RAW_URL, "repository.json" )
    g_channel_settings['CHANNEL_REPOSITORY_FILE'] = os.path.join( CURRENT_DIRECTORY, "repository.json" )

    # The default user preferences file
    g_channel_settings['USER_SETTINGS_FILE'] = "Preferences.sublime-settings"

    # You can specify for some packages to be popped out from the list and being installed by
    # first/last in the following order presented.
    #
    # The package `PackagesManager` need to installed last, otherwise soon as it is installed it
    # will ask the user restart Sublime Text due the installation of missing dependencies. However
    # if the user restarts Sublime Text on the middle of the installation, the installation is
    # stopped. The user should only stop the installation because he wants to, not because
    # `PackagesManager` asked to restart.
    #
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
    g_channel_settings['PACKAGES_TO_INSTALL_FIRST'] = \
    [
        "Notepad++ Color Scheme",
    ]

    g_channel_settings['PACKAGES_TO_INSTALL_LAST'] = \
    [
        "0_settings_loader",
        "Default",
        "BetterFindBuffer",
        "A File Icon",
        "PackagesManager",
    ]

    # Packages which are not allowed to be selected by the user while choosing the packages to not
    # be installed. Useful for packages which are required for the channel maintainability.
    g_channel_settings['FORBIDDEN_PACKAGES'] = \
    [
        "0_settings_loader",
        "ChannelManager",
        CURRENT_PACKAGE_NAME,
        "Notepad++ Color Scheme",
        "PackagesManager",
    ]

    # Packages which you do want to install when reading the `.gitmodules` packages list (stable)
    g_channel_settings['PACKAGES_TO_NOT_INSTALL_STABLE'] = \
    [
        "User",
        "AmxxChannel",
        "PackagesManager",
        "SublimeLinter",
        "SublimeLinter-javac",
        "OverrideEditSettingsDefaultContents",
    ]

    # Packages which you do want to install when reading the `.gitmodules` packages list (development)
    g_channel_settings['PACKAGES_TO_NOT_INSTALL_DEVELOPMENT'] = \
    [
    ]

    # Packages which must not be installed on the stable version and must be disabled by default on
    # the development version.
    g_channel_settings['PACKAGES_TO_IGNORE_ON_DEVELOPMENT'] = \
    [
        "All Autocomplete",
        "Anaconda",
        "ApplySyntax",
        "BracketHighlighter",
        "C++ Completions",
        "C++ Snippets",
        "C++ Starting Kit",
        "ColorHelper",
        "DictionaryAutoComplete",
        "FileManager",
        "Find++",
        "FuzzyFilePath",
        "Gist",
        "Git",
        "GitGutter",
        "GotoLastEditEnhanced",
        "Javatar",
        "Jedi - Python autocompletion",
        "Local History",
        "Matlab Completions",
        "MatlabFilenameAutoComplete",
        "MySQL Snippets",
        "Project Specific Syntax Settings",
        "Qt Completions for C++",
        "ScopeAlways",
        "sublime-text-2-buildview",
        "SublimeCodeIntel",
        "SublimeLinter",
        "SublimeLinter-javac",
        "SyncedSideBar",
        "TypeScript",
        "Vintage",
        "WordHighlight",
    ]

    # The files of the `Default.sublime-package` you are installing
    g_channel_settings['DEFAULT_PACKAGES_FILES'] = \
    [
        ".gitignore",
        ".no-sublime-package",
        "Context.sublime-menu",
        "Distraction Free.sublime-settings",
        "Find Results.hidden-tmLanguage",
        "Main.sublime-menu",
        "README.md",
        "Sublime Text Settings.sublime-settings",
        "Tab Context.sublime-menu",
        "install_package_control.py",
        "platform_edit_settings.py",
        "synced_side_bar_watcher.py",
        "transpose.py",
    ]

    # Print all their values for debugging
    variables = \
    [
        "%-30s: %s" % ( variable_name, g_channel_settings[variable_name] )
        for variable_name in g_channel_settings.keys()
    ]

    # print("\nImporting %s settings... \n%s" % ( str(datetime.datetime.now())[0:19], "\n".join( sorted(variables) ) ))


