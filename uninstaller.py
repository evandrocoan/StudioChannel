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
import time
import shutil
import zipfile
import tempfile

import io
import re
import json
import shlex
import stat
import threading
import contextlib
import textwrap

g_is_already_running = False

from . import settings

from .settings import CURRENT_DIRECTORY
from .settings import CURRENT_PACKAGE_NAME

from ChannelManager import studio_uninstaller


# Import the debugger
from debug_tools import Debugger

# Debugger settings: 0 - disabled, 127 - enabled
log = Debugger( 127, os.path.basename( __file__ ) )

log( 2, "..." )
log( 2, "..." )
log( 2, "Debugging" )
log( 2, "CURRENT_DIRECTORY_: " + CURRENT_DIRECTORY )


def unpack_settings():
    """
        How to import python class file from same directory?
        https://stackoverflow.com/questions/21139364/how-to-import-python-class-file-from-same-directory

        Global variable is not updating in python
        https://stackoverflow.com/questions/30392157/global-variable-is-not-updating-in-python
    """
    global g_channel_settings
    g_channel_settings = settings.g_channel_settings


def uninstall():
    """
        Used for testing purposes while developing this package.
    """
    unpack_settings()

    sublime.active_window().run_command( "show_panel", {"panel": "console", "toggle": False} )
    studio_uninstaller.main( g_channel_settings )


