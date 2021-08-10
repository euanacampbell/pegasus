from requests import get
import subprocess


class update:
    """Format a SQL query"""

    def __init__(self):
        self.__VERSION__ = 'v0.5'

    def __run__(self, params=None):

        if params[0] == 'check':
            self.check_for_updates(True)
        elif params[0] == 'run':
            self.update_pegasus()
        else:
            print('update command not recognised.')

    def check_for_updates(self, print_toggle=False):

        response = get(
            "https://api.github.com/repos/euanacampbell/pegasus/releases/latest")

        latest_version = response.json()["tag_name"]

        if latest_version != self.__VERSION__:
            print(
                f'\nYou are using Pegasus version {self.__VERSION__}; however, version {latest_version} is available.')
            print("Use command 'update run' to update to the latest version.")
        elif latest_version == self.__VERSION__ and print_toggle:
            print(
                f'\nYou are using the latest version of Pegasus ({self.__VERSION__}).')

    def update_pegasus(self):

        output = subprocess.check_output(
            ["git", "pull"]).strip()

        print(output.decode("utf-8"))


if __name__ == "__main__":

    u = update()

    u.check_for_updates()
