from requests import get
import subprocess
import sys


class update:
    """Check if you're running the latest version and update to the latest release."""

    def __init__(self):
        self.__VERSION__ = 'v0.15'
        self.latest_version = 'v0.15'

    def __run__(self, params=None):
        if len(params) == 0:
            return "did you mean to use 'update check' or 'update run'?"
        if params[0] == 'check':
            return self.check_for_updates(print_toggle=True)

        elif params[0] == 'run':
            return self.update_pegasus()
        else:
            return "did you mean to use 'update check' or 'update run'?"

    def is_latest_version(self):

        response = get(
            "https://api.github.com/repos/euanacampbell/pegasus/releases/latest")

        latest_version = response.json()["tag_name"]

        if latest_version != self.__VERSION__:
            self.latest_version = latest_version
            return False
        else:
            self.latest_version = latest_version
            return True

    def check_for_updates(self, print_toggle=False):

        is_latest = self.is_latest_version()

        if is_latest:
            return f'\nYou are using the latest version of Pegasus ({self.__VERSION__}).'
        elif is_latest and print_toggle == True:
            return f"\nYou are using Pegasus version {self.__VERSION__}; however, version {self.latest_version} is the latest available. Use command 'update run' to update to the latest version."

    def update_pegasus(self):

        if self.is_latest_version():
            return f'\nYou are using the latest version of Pegasus ({self.__VERSION__}).'
        else:
            subprocess.check_output(
                ["git", "pull"]).strip()

            return '\nPegasus is updating. If you are running the web version, it will auto-restart. If you are running the terminal version, please close and re-open Pegasus.'
