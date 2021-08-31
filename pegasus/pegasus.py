from pegasus.modules.format import format
from pegasus.modules.sql import sql
from pegasus.modules.lockscreen import lockscreen
from pegasus.modules.update import update

import os
import sys
from os import listdir
from os.path import isfile, join
import traceback
from rich.traceback import install


class Pegasus:

    def __init__(self):
        self.result = None

    def format_input(self, user_input):
        """Takes input from user, separates command and params and returns them"""

        command = user_input.split(' ')[0]

        try:
            param = user_input.split(' ')[1:]
        except:
            param = None

        return {
            'command': command,
            'param': param
        }

    def run_command(self, user_input):

        formatted_input = self.format_input(user_input)
        self.user_input = user_input
        command = formatted_input['command']
        param = formatted_input['param']

        system_commands = {
            'help': self.help,
            'exit': self.exit,
            'clear': self.clear
        }

        # run built-in commands
        if command in system_commands:
            result = system_commands[command]()
            return self.build_return(result)

        # check the command exists
        try:
            module = globals()[command]()
        except KeyError as e:
            message = f"Error: '{command}' command not recognised, run 'help' to see available commands."
            return self.build_return(message, type='error')

        # catch any errors in the command/module
        try:
            module_result = module.__run__(param)
            return self.build_return(module_result)
        except Exception as e:
            return self.build_return(str(e), type='error')

    def help(self):
        current_path = os.path.dirname(os.path.abspath(__file__)) + '/modules'
        files = [f[:-3] for f in listdir(current_path) if isfile(
            join(current_path, f)) and '__init__' not in f and '.py' in f]

        help_commands = []
        for file in files:
            try:
                instance = globals()[file]()
                description = instance.__doc__
            except KeyError:
                description = f'Error, not imported.'

            help_commands.append([file, description])

        return help_commands

    def exit(self):
        sys.exit()

    def clear(self):
        print('\x1b[2J')

    def build_return(self, results, type=None):

        if not type:
            type = self.result_type(results)

        return {
            'command': self.user_input,
            'results': results,
            'result_type': type
        }

    def result_type(self, result):

        if type(result) is str:
            result_type = 'string'
        elif type(result) is list:
            result_type = 'list'
            if type(result[0]) is dict:
                result_type = 'listofdict'
            elif type(result[0]) is list:
                result_type = 'listoflist'
        elif type(result) is dict:
            result_type = 'dict'
        else:
            result_type = 'error'

        return result_type


if __name__ == "__main__":

    while True:
        text_input = input('\ncommand: ')

        p = Pegasus().run_command(text_input)
