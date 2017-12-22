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
# Studio Channel, assist the user on the Channel Studio uninstallation
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

import os
import threading


g_is_already_running = False
from . import settings

from .settings import CURRENT_PACKAGE_ROOT_DIRECTORY
from .settings import CURRENT_PACKAGE_NAME

from channel_manager import channel_uninstaller
from channel_manager.channel_utilities import wrap_text


# When there is an ImportError, means that Package Control is installed instead of PackagesManager,
# or vice-versa. Which means we cannot do nothing as this is only compatible with PackagesManager.
try:
    from package_control.thread_progress import ThreadProgress

except ImportError:
    from PackagesManager.packagesmanager.thread_progress import ThreadProgress


from python_debug_tools import Debugger

# Debugger settings: 0 - disabled, 127 - enabled
log = Debugger( 127, os.path.basename( __file__ ) )

# log( 2, "..." )
# log( 2, "..." )
# log( 2, "Debugging" )
# log( 2, "CURRENT_PACKAGE_ROOT_DIRECTORY_: " + CURRENT_PACKAGE_ROOT_DIRECTORY )


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


def unpack_settings():
    """
        How to import python class file from same directory?
        https://stackoverflow.com/questions/21139364/how-to-import-python-class-file-from-same-directory

        Global variable is not updating in python
        https://stackoverflow.com/questions/30392157/global-variable-is-not-updating-in-python
    """
    global g_channel_settings
    g_channel_settings = settings.g_channel_settings


class StartInstallationWizardThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """
            Python thread exit code
            https://stackoverflow.com/questions/986616/python-thread-exit-code
        """

        if is_allowed_to_run():
            unpack_settings()
            wizard_thread = InstallationWizardThread()

            wizard_thread.start()
            ThreadProgress( wizard_thread, 'Running the %s Installation Wizard' % CURRENT_PACKAGE_NAME,
                    'The %s Installation Wizard finished' % CURRENT_PACKAGE_NAME )

            wizard_thread.join()

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


def run_the_installation_wizard(step=1):

    if show_program_description():
        uninstall()


def show_program_description():
    uninstall_button = "Completely Uninstall Everything"

    lines = \
    [
        wrap_text( """\
        Welcome to the %s Uninstallation Wizard.

        It is recommended to backup your Sublime Text's current settings and packages before
        uninstalling this, either for the Stable or Development version.

        Now you got the chance to go and backup everything. No hurries. When you finished your
        backup, you can come back here and click on the `%s` button to start now the uninstallation
        process for all the %s packages.

        This will uninstall all Sublime Text Packages the installer has installed on your computer,
        however if already there were some of these packages installed, your current version will
        not be downgraded to the version you used before installing this package. After running this
        wizard, you need to reinstall the packages you want to be restored to their original
        versions.

        If you had cancelled the Installation Wizard before it completed installing all its
        packages, or some cases when the installer is not complete, the PackagesManager could not be
        installed (as it is installed by last). Then the Uninstaller cannot run as it requires
        PackagesManager instead of Package Control. Therefore on these cases the user is required to
        install manually PackagesManager, before running the %s uninstaller.

        Click on the `Cancel` button if you want give up from installing the %s.
        """ % ( CURRENT_PACKAGE_NAME, uninstall_button, CURRENT_PACKAGE_NAME,
                CURRENT_PACKAGE_NAME, CURRENT_PACKAGE_NAME ) ),
    ]

    return sublime.ok_cancel_dialog( "\n".join( lines ), uninstall_button )


def uninstall():
    """
        Used for testing purposes while developing this package.
    """
    unpack_settings()
    channel_uninstaller.main( g_channel_settings, True )

