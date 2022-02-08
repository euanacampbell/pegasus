
from pegasus.pegasus import Pegasus

from rich.console import Console
from rich.table import Table
from rich import print
from tabulate import tabulate


def print_table(body, columns=None, better_tables=False):

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


better_tables = False
while True:

    text_input = input('\ncommand: ')

    if text_input == 'toggle: table_format':
        better_tables = not better_tables
        print(f'\nTable formatting now set to {better_tables}')
        continue

    response = Pegasus().run_command(text_input)

    for item in response['response']:

        if item['type'] in ('string', 'int', 'error'):

            content = str(item['content'])

            for i in ['%end_border%', '%end_row%', '%start_border%', '%start_row%', '%header%']:
                content = content.replace(i, '')

            if content == '':
                continue

            print(f"\n{content}")
        elif item['type'] == 'dictoflist':
            print_table(item['content']['results'],
                        columns=item['content']['columns'], better_tables=better_tables)

        elif item['type'] == 'listoflist':
            print_table(item['content'], better_tables=better_tables)

        elif item['type'] == 'list':
            for i in item:
                print(i)
        else:
            item_type = item['type']
            print(f'{item_type} not recognised')
