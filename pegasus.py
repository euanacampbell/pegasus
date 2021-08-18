from modules.jsonformat import jsonformat
from modules.sqlformat import sqlformat
from modules.format import format
from modules.listformat import listformat
from modules.sql import sql
from modules.lockscreen import lockscreen
from modules.update import update
from modules.xmlformat import xmlformat

import os
import sys
from os import listdir
from os.path import isfile, join
import traceback
from rich.traceback import install
install()

update().check_for_updates()

while True:
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
                description = f'Unavailable: Not imported in main'
            print(f' - {description}')

    elif command == 'exit':
        sys.exit()
    elif command == 'reload':
        continue
    elif command == 'clear':
        print('\x1b[2J')
    else:
        try:
            module = globals()[command]()
        except KeyError as e:
            print('Unavailable: Not imported in main')
            continue
        except:
            traceback.print_exc()
            continue

        try:
            module.__run__(param)
        except:
            traceback.print_exc()
