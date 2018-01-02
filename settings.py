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

# from channel_manager.channel_utilities import print_all_variables_for_debugging
# print_all_variables_for_debugging( g_channelSettings )
# import sublime_plugin
# sublime_plugin.reload_plugin( "channel_manager.channel_utilities" )

from channel_manager.channel_utilities import clean_urljoin
from channel_manager.channel_utilities import run_channel_setup

CURRENT_PACKAGE_FILE   = os.path.dirname( os.path.realpath( __file__ ) )
PACKAGE_ROOT_DIRECTORY = CURRENT_PACKAGE_FILE.replace( ".sublime-package", "" )
CURRENT_PACKAGE_NAME   = os.path.basename( PACKAGE_ROOT_DIRECTORY )

def plugin_loaded():
    global g_channelSettings
    CHANNEL_RAW_URL = "https://raw.githubusercontent.com/evandrocoan/SublimeStudioChannel/master/"

    g_channelSettings = {}
    g_channelSettings['CHANNEL_ROOT_URL']    = "https://github.com/evandrocoan/ITE"
    g_channelSettings['DEFAULT_CHANNEL_URL'] = "https://packagecontrol.io/channel_v3.json"

    g_channelSettings['CHANNEL_FILE_URL']  = clean_urljoin( CHANNEL_RAW_URL, "channel.json" )
    g_channelSettings['CHANNEL_FILE_PATH'] = os.path.join( PACKAGE_ROOT_DIRECTORY, "channel.json" )

    g_channelSettings['CHANNEL_REPOSITORY_URL']  = clean_urljoin( CHANNEL_RAW_URL, "repository.json" )
    g_channelSettings['CHANNEL_REPOSITORY_FILE'] = os.path.join( PACKAGE_ROOT_DIRECTORY, "repository.json" )

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
    g_channelSettings['PACKAGES_TO_INSTALL_FIRST'] = \
    [
        "Notepad++ Color Scheme",
    ]

    g_channelSettings['PACKAGES_TO_INSTALL_LAST'] = \
    [
        "0_settings_loader",
        "Default",
        "BetterFindBuffer",
        "A File Icon",
        "PackagesManager",
    ]

    g_channelSettings['FORBIDDEN_PACKAGES'] = \
    [
        "0_settings_loader",
        "ChannelManager",
        "Notepad++ Color Scheme",
        "PackagesManager",
    ]

    g_channelSettings['DEFAULT_PACKAGE_FILES'] = \
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

    g_channelSettings['PACKAGES_TO_NOT_INSTALL_STABLE'] = \
    [
        "User",
        "AmxxChannel",
        "PackagesManager",
        "UnitTesting",
        "ColorSchemeUnit",
        "OverrideEditSettingsDefaultContents",
    ]

    g_channelSettings['PACKAGES_TO_NOT_INSTALL_DEVELOPMENT'] = \
    [
    ]

    g_channelSettings['PACKAGES_TO_INSTALL_EXCLUSIVELY'] = \
    [
    ]

    g_channelSettings['PACKAGES_TO_IGNORE_ON_DEVELOPMENT'] = \
    [
        "Anaconda",
        "ApplySyntax",
        "BracketHighlighter",
        "BuildView",
        "C++ Completions",
        "C++ Qt Completions",
        "C++ Snippets",
        "CodeIntel",
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
        "JediPythonAutoCompletion",
        "LocalHistory",
        "MatlabCompletions",
        "MatlabFilenameAutoComplete",
        "MySQLSnippets",
        "ProjectSpecificSyntax",
        "ScopeAlways",
        "SublimeLinter",
        "SublimeLinter-javac",
        "SyncedSideBar",
        "TypeScript",
        "Vintage",
        "WordHighlight",
    ]

    g_channelSettings['CHANNEL_VERSIONS_DESCRIPTIONS'] = """\
        There are two versions of the channel. Each one of them has its proper usage depending on
        your plans. The Stable Version is the most tested and trusted set of packages to be
        installed. It contains all the packages which can be actively enabled and used on daily
        basis usage and it requires the latest Stable Build of Sublime Text available, as builds
        3126 and 3143.

        The Development Version has the same packages as the Stable Version, however it also
        installs candidate packages to the Stable Version, i.e., packages which are not thoroughly
        tested. Some of them are expected to have serious bugs as crash your Sublime Text,
        significantly slow down the Sublime Text performance, i.e., create great problems. Due this,
        these extra packages are by default added to your `ignored_packages` settings. You should
        only enable them when you are attempting to fix their problems or test them.

        For both Stable and Development versions, your Sublime Text's Package Control will be
        uninstalled and replaced by the its forked version called `PackagesManager`. Now on, you
        should look for the package `PackagesManager` to install and uninstalling packages. The
        Stable Version installs all packages by PackagesManager as they normally are installed by
        the Sublime Text's Package Control. Therefore they require smaller amount of space in your
        file system. It should be about 60MB of data, on the last time checked.

        Now the Development Version installs all your packages by `git`, therefore you need to have
        git installed in your system in order to install the development Version. Also due this, the
        Development Version requires much more file system space. The last time checked it required
        about 600MB of free space. Notice also, the Development Version requires the latest
        Development Build of Sublime Text available, as builds 3141 and 3147.
        """

    run_channel_setup( g_channelSettings, CURRENT_PACKAGE_FILE )

