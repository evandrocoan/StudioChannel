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
import sublime

from channel_manager.channel_utilities import clean_urljoin
from channel_manager.channel_utilities import run_channel_setup

CURRENT_PACKAGE_ROOT_DIRECTORY = os.path.dirname( os.path.realpath( __file__ ) ).replace( ".sublime-package", "" )
CURRENT_PACKAGE_NAME           = os.path.basename( CURRENT_PACKAGE_ROOT_DIRECTORY )

def plugin_loaded():
    global g_channel_settings
    CHANNEL_RAW_URL = "https://raw.githubusercontent.com/evandrocoan/StudioChannel/master/"

    g_channel_settings = {}
    g_channel_settings['CHANNEL_ROOT_URL']    = "https://github.com/evandrocoan/SublimeTextStudio"
    g_channel_settings['DEFAULT_CHANNEL_URL'] = "https://packagecontrol.io/channel_v3.json"

    g_channel_settings['CHANNEL_FILE_URL']  = clean_urljoin( CHANNEL_RAW_URL, "channel.json" )
    g_channel_settings['CHANNEL_FILE_PATH'] = os.path.join( CURRENT_PACKAGE_ROOT_DIRECTORY, "channel.json" )

    g_channel_settings['CHANNEL_REPOSITORY_URL']  = clean_urljoin( CHANNEL_RAW_URL, "repository.json" )
    g_channel_settings['CHANNEL_REPOSITORY_FILE'] = os.path.join( CURRENT_PACKAGE_ROOT_DIRECTORY, "repository.json" )

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

    g_channel_settings['FORBIDDEN_PACKAGES'] = \
    [
        "0_settings_loader",
        "ChannelManager",
        CURRENT_PACKAGE_NAME,
        "Notepad++ Color Scheme",
        "PackagesManager",
    ]

    g_channel_settings['DEFAULT_PACKAGE_FILES'] = \
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

    g_channel_settings['PACKAGES_TO_NOT_INSTALL_STABLE'] = \
    [
        "User",
        "AmxxChannel",
        "PackagesManager",
        "UnitTesting",
        "ColorSchemeUnit",
        "OverrideEditSettingsDefaultContents",
    ]

    g_channel_settings['PACKAGES_TO_NOT_INSTALL_DEVELOPMENT'] = \
    [
    ]

    g_channel_settings['PACKAGES_TO_INSTALL_EXCLUSIVELY'] = \
    [
    ]

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

    run_channel_setup( g_channel_settings, CURRENT_PACKAGE_NAME, CURRENT_PACKAGE_ROOT_DIRECTORY )

    # from channel_manager.channel_utilities import print_all_variables_for_debugging
    # print_all_variables_for_debugging
    # import sublime_plugin
    # sublime_plugin.reload_plugin( "channel_manager.channel_utilities" )

