
from cProfile import run
from pegasus_client.pegasus_handler import PegasusHandler

from rich.console import Console
from rich.table import Table
from rich import print
from tabulate import tabulate
from flask import Flask

from pegasus_client.routes.sql_routes import sql_routes
from pegasus_client.routes.core import core_routes
from pegasus_client.routes.error_handling import error_routes


class Pegasus:

    def __init__(self, run_type='web', sql_config_location='', port_number=7342):

        if run_type == 'web':
            self.run_web(port_number)
        elif run_type == 'terminal':
            self.run_terminal()
        else:
            print('run type not recognised')

    def run_web(self, port_number):

        #  initialise flask
        app = Flask(__name__)
        app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

        # import blueprint routes
        app.register_blueprint(sql_routes)
        app.register_blueprint(core_routes)
        app.register_blueprint(error_routes)

        # start it up!
        app.run(host='127.0.0.1', port=port_number)

    def print_table(self, body, columns=None, better_tables=False):

        if better_tables:
            console = Console()
            table = Table(show_header=True, header_style="bold")

            table.row_styles = ["none", "dim"]

            if columns:
                for col in columns:
                    table.add_column(col)

            for row in body:
                table.add_row(*row)

            console.print(table)
        else:
            if columns:
                print(tabulate(body,
                               headers=columns, tablefmt="pretty"))
            else:
                print(tabulate(body, tablefmt="pretty"))

    def run_terminal(self):

        better_tables = False

        while True:

            text_input = input('\ncommand: ')

            if text_input == 'toggle: table_format':
                better_tables = not better_tables
                print(f'\nTable formatting now set to {better_tables}')
                continue

            response = PegasusHandler().run_command(text_input)

            for item in response['response']:

                if item['type'] in ('string', 'int', 'error'):

                    content = str(item['content'])

                    for i in ['%end_border%', '%end_row%', '%start_border%', '%start_row%', '%header%']:
                        content = content.replace(i, '')

                    if content == '':
                        continue

                    print(f"\n{content}")
                elif item['type'] == 'dictoflist':
                    self.print_table(item['content']['results'],
                                     columns=item['content']['columns'], better_tables=better_tables)

                elif item['type'] == 'listoflist':
                    self.print_table(
                        item['content'], better_tables=better_tables)

                elif item['type'] == 'list':
                    for i in item:
                        print(i)
                else:
                    item_type = item['type']
                    print(f'{item_type} not recognised')


class options:

    def __init__(self):

        self.run_type = run_type
        self.sql_config_location = sql_config_location
