from modules.format import format
from modules.sql import sql
from modules.lockscreen import lockscreen
from modules.update import update

import os
import sys
from os import listdir
from os.path import isfile, join
import traceback
from rich.traceback import install


def loop():
    print('')
    # input
    text_input = input('command: ')
    command = text_input.split(' ')[0]
    try:
        param = text_input.split(' ')[1:]
    except:
        param = None

    if command == 'help':
        current_path = os.path.dirname(os.path.abspath(__file__)) + '/modules'
        files = [f[:-3] for f in listdir(current_path) if isfile(
            join(current_path, f)) and '__init__' not in f and '.py' in f]
        for fil in files:
            print('')
            print(fil)
            try:
                instance = globals()[fil]()
                description = instance.__doc__

            except KeyError:
                description = f'Error: Not imported in main'
            print(f' - {description}')

    elif command == 'exit':
        sys.exit()
    elif command == 'reload':
        return
    elif command == 'clear':
        print('\x1b[2J')
    else:
        module = globals()[command]()
        try:
            module = globals()[command]()
        except KeyError as e:
            print(
                f"Error: '{command}' command not recognised, check it has been imported.")

            return
        except:
            traceback.print_exc()
            return

        try:
            module.__run__(param)
        except:
            traceback.print_exc()
    return 'success'


if __name__ == "__main__":
    install()

    update().check_for_updates()

    while True:
        loop()
