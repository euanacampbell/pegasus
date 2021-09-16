from requests import get
import subprocess
import sys


class update:
    """Check if you're running the latest version and update to the latest release."""

    def __init__(self):
        self.__VERSION__ = 'v0.14'

    def __run__(self, params=None):
        if len(params) == 0:
            return "did you mean to use 'update check' or 'update run'?"
        if params[0] == 'check':
            return self.check_for_updates(True)

        elif params[0] == 'run':
            return self.update_pegasus()
        else:
            return 'update command not recognised.'

    def get_latest_version(self):

        response = get(
            "https://api.github.com/repos/euanacampbell/pegasus/releases/latest")

        latest_version = response.json()["tag_name"]

        return latest_version

    def check_for_updates(self, print_toggle=False):

        latest_version = self.get_latest_version()

        if latest_version != self.__VERSION__:
            return f"\nYou are using Pegasus version {self.__VERSION__}; however, version {latest_version} is the latest available. Use command 'update run' to update to the latest version."

        elif latest_version == self.__VERSION__ and print_toggle == True:
            return f'\nYou are using the latest version of Pegasus ({self.__VERSION__}).'

    def update_pegasus(self):

        output = subprocess.check_output(
            ["git", "pull"]).strip()

        return '\nplease restart for updates to apply'


if __name__ == "__main__":

    u = update()

    u.check_for_updates()