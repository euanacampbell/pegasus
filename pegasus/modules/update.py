from requests import get
import urllib
import zipfile
import os
import shutil
from distutils.dir_util import copy_tree


class update:
    """Check if you're running the latest version and update to the latest release."""

    def __init__(self):
        self.__VERSION__ = 'v0.17'

        self.download_url = 'https://github.com/euanacampbell/pegasus/archive/refs/heads/main.zip'

    def __run__(self, params=None):

        if params == [''] or params[0] == 'check':
            return self.check_for_updates(print_toggle=True)
        elif params[0] == 'run':
            return self.update_pegasus()
        else:
            return "Did you mean to use 'update check' or 'update run'?"

    def get_latest_version(self):

        response = get(
            "https://api.github.com/repos/euanacampbell/pegasus/releases/latest")

        return response.json()["tag_name"]

    def is_latest_version(self):

        latest_version = self.get_latest_version()

        if latest_version != self.__VERSION__:
            return False
        else:
            return True

    def check_for_updates(self, print_toggle=False):

        is_latest = self.is_latest_version()

        if is_latest:
            return f'\nYou are using the latest version of Pegasus ({self.__VERSION__}).'
        elif is_latest and print_toggle == True:
            return f"\nYou are using Pegasus version {self.__VERSION__}; however, version {self.get_latest_version()} is the latest available. Use command 'update run' to update to the latest version."

    def update_pegasus(self):

        if self.is_latest_version():
            return f'\nYou are using the latest version of Pegasus ({self.__VERSION__}).'
        else:
            self.perform_update()

            return '\nPegasus is updating. If you are running the web version, it will auto-restart. If you are running the terminal version, please close and re-open Pegasus.'

    def subcommands(self):

        return ['check', 'run']

    def perform_update(self):

        # download file
        urllib.request.urlretrieve(
            self.download_url, self.download_url.split('/')[-1])

        # unzip downloaded file
        with zipfile.ZipFile('main.zip', 'r') as zip_ref:
            zip_ref.extractall()

        # copy files
        to_copy = ['pegasus_terminal.py',
                   'pegasus_web.py',
                   'pegasus_terminal.py',
                   'pegasus/pegasus.py',
                   'pegasus/modules/generic/clipboard.py',
                   'pegasus/modules/connection.py',
                   'pegasus/modules/example.py',
                   'pegasus/modules/format.py',
                   'pegasus/modules/sql.py',
                   'pegasus/modules/update.py',
                   'pegasus/pegasus.py',
                   'pegasus/pegasus.py',
                   'routes',
                   'templates',
                   'static',
                   'requirements.txt',
                   'Readme.md'
                   ]

        for file in to_copy:

            src = f'pegasus-main/{file}'

            if '.' in file:  # file
                shutil.copyfile(src, file)
            else:  # folder
                copy_tree(src, file)

        # delete downloaded files
        os.remove('main.zip')
        shutil.rmtree('pegasus-main')


if __name__ == '__main__':
    u = update()

    u.download_files()
