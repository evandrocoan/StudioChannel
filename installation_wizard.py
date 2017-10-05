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
import json
import shlex
import stat
import threading
import contextlib


g_is_already_running = False

from .settings import CURRENT_DIRECTORY
from .settings import g_channel_settings

from PackagesManager.packagesmanager import cmd
from PackagesManager.packagesmanager.download_manager import downloader

from PackagesManager.packagesmanager.package_manager import PackageManager
from PackagesManager.packagesmanager.thread_progress import ThreadProgress
from PackagesManager.packagesmanager.package_disabler import PackageDisabler
from PackagesManager.packagesmanager.commands.remove_package_command import RemovePackageThread


# Import the debugger
from debug_tools import Debugger

# Debugger settings: 0 - disabled, 127 - enabled
log = Debugger( 127, os.path.basename( __file__ ) )

log( 2, "..." )
log( 2, "..." )
log( 2, "Debugging" )
log( 2, "CURRENT_DIRECTORY_: " + CURRENT_DIRECTORY )


def main():
    """
        Before calling this installer, the `Package Control` user settings file, must have the
        Studio Channel file set before the default channel key `channels`.

        Also the current `Package Control` cache must be cleaned, ensuring it is downloading and
        using the Studio Channel repositories/channel list.
    """
    log( 2, "Entering on %s main(0)" % CURRENT_PACKAGE_NAME )

    wizard_thread = StartInstallationWizardThread()
    wizard_thread.start()


class StartInstallationWizardThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """
            Python thread exit code
            https://stackoverflow.com/questions/986616/python-thread-exit-code
        """

        if is_allowed_to_run():
            wizard_thread = InstallationWizardThread()

            wizard_thread.start()
            ThreadProgress( wizard_thread, 'Running the Studio Installation Wizard',
                    'The Installation Wizard finished' )

            wizard_thread.join()
            check_uninstalled_packages()

        global g_is_already_running
        g_is_already_running = False


def is_allowed_to_run():
    global g_is_already_running

    if g_is_already_running:
        print( "You are already running a command. Wait until it finishes or restart Sublime Text" )
        return False

    g_is_already_running = True
    return True


class InstallationWizardThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        log( 2, "Entering on %s run(1)" % self.__class__.__name__ )
        run_the_installation_wizard()


def run_the_installation_wizard():

    if start_the_installation():
        show_program_description()

    else:

        if show_goodbye_message():
            run_the_installation_wizard()


def show_program_description():
    lines = \
    [
        "Thank you for choosing the %s. This is" % CURRENT_PACKAGE_NAME
    ]

    return sublime.ok_cancel_dialog( "\n".join( lines ), "Yes, I do agree with it" )


def show_goodbye_message():
    ok_button_text = "Return to the wizard"

    lines = \
    [
        "Thank you for looking to install the %s," % CURRENT_PACKAGE_NAME,
        "but as you do not agree with its usage license,",
        "the %s need to be uninstalled as without"  % CURRENT_PACKAGE_NAME,
        "installing, it does nothing else useful for you.",
        "",
        "If you want to consider installing it, click on the button",
        "`%s` to go back and try again. Otherwise" % ok_button_text,
        "click on the `Cancel` button and uninstall the %s."  % CURRENT_PACKAGE_NAME,
        "",
        "If you wish to install the %s later, you can"  % CURRENT_PACKAGE_NAME,
        "go to the menu `Preferences -> Packages -> %s`" % CURRENT_PACKAGE_NAME,
        "and select the option `Run Installation Wizard`, to run this",
        "Installer Wizard again.",
        "",
        "If you wish to install the %s later, after"  % CURRENT_PACKAGE_NAME,
        "uninstalling it, you can just install this package again.",
    ]

    return sublime.ok_cancel_dialog( "\n".join( lines ), ok_button_text )


def start_the_installation():
    lines = \
    [
        "Welcome to the %s Installation Wizard." % CURRENT_PACKAGE_NAME,
        "",
        "The installed packages by this wizard, in addition to each one",
        "own license, are distributed under the following conditions:",
        "",
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF",
        "ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED",
        "TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A",
        "PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT",
        "SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR",
        "ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN",
        "ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,",
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE",
        "OR OTHER DEALINGS IN THE SOFTWARE.",
        "",
        "On the following address you can find the list of all",
        "distributed software which this conditions applies to:",
        "<%s#License>" % g_channel_settings['studio_main_url'],
        "",
        "---",
        "",
        "Do you agree with these conditions for using this software?",
    ]

    return sublime.ok_cancel_dialog( "\n".join( lines ), "Yes, I do agree with it" )


def is_the_first_load_time():
    """
        Check whether this is the first time the user is running it. If so, then start the
        installation wizard to install the channel or postpone the installation process.

        If the installation is postponed, then the user must to manually start it by running its
        command on the command palette or in the preferences menu.
    """
    return True


if __name__ == "__main__":
    main()


def plugin_loaded():

    if is_the_first_load_time():
        # main()
        pass

