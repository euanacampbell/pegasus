from pegasus.modules.format import format
from pegasus.modules.sql import sql
from pegasus.modules.update import update
from pegasus.modules.test_display import test_display

import os
import sys
from os import listdir
from os.path import isfile, join
import yaml
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

        sub_commands_lookup = self.sub_commands()
        sub_commands = list(sub_commands_lookup.keys())

        if command in globals():
            module = globals()[command]()
        elif command in sub_commands:  # sub-commands
            param.insert(0, command)
            command = sub_commands_lookup[command]
            module = globals()[command]()
        else:
            return self.build_return(f"'{command}' command not recognised, run 'help' to see available commands.", error='error')

        # catch any errors in the command/module
        # module_result = module.__run__(param)
        # return self.build_return(module_result)

        try:
            module_result = module.__run__(param)
            return self.build_return(module_result)
        except Exception as e:
            return self.build_return(str(e), error='error')

    def help(self):

        help_commands = []
        for file in self.available_modules():
            sub = []

            # get description
            try:
                instance = globals()[file]()
                description = instance.__doc__
                for sub_command in instance.subcommands():
                    sub.append(
                        [sub_command, f"Inherited from {file}."])
            except KeyError:
                description = f'Error, not imported.'
            except AttributeError:
                pass

            help_commands.append([file, description])
            if len(sub) > 0:
                help_commands = help_commands + sub

        return [help_commands]

    def sub_commands(self):

        sub_commands = {}

        for file in self.available_modules():
            instance = globals()[file]()

            try:
                for command in instance.subcommands():
                    sub_commands[command] = file
            except AttributeError:
                pass

        return sub_commands

    def exit(self):
        sys.exit()

    def available_modules(self):
        current_path = os.path.dirname(os.path.abspath(__file__)) + '/modules'
        files = [f[:-3] for f in listdir(current_path) if isfile(
            join(current_path, f)) and '__init__' not in f and '.py' in f]

        return files

    def clear(self):
        print('\x1b[2J')
        return('')

    def build_return(self, response, error=None):

        if type(response) not in (dict, list):
            response = [response]

        built_response = []
        for item in response:
            if type(item) == int:
                item = str(item)
            new_item = {
                "type": error or self.result_type(item),
                "content": item
            }

            built_response.append(new_item)

        return {
            'command': self.user_input,
            'available_commands': self.available_commands(),
            'response': built_response,
            'error': error
        }

    def result_type(self, result):

        if type(result) is str:
            result_type = 'string'
        elif type(result) is list:
            result_type = 'list'
            if type(result[0]) is list:
                result_type = 'listoflist'
        elif type(result) is dict:
            result_type = 'dict'
            if type(result[next(iter(result))]) is list:
                result_type = 'dictoflist'
        else:
            result_type = 'error'

        return result_type

    def available_commands(self):

        commands = self.help()[0]
        commands = [command[0] for command in commands]

        return commands


if __name__ == "__main__":

    while True:
        text_input = input('\ncommand: ')

        p = Pegasus().run_command(text_input)
