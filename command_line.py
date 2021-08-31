
from pegasus.pegasus import Pegasus

from rich.console import Console
from rich.table import Table
from rich import print
from tabulate import tabulate


def print_table(body, columns=None):
    better_tables = False
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
        print(tabulate(body,
                       headers=columns, tablefmt="pretty"))


while True:

    text_input = input('\ncommand: ')

    response = Pegasus().run_command(text_input)

    for item in response['response']:
        if item['type'] in ('string', 'int', 'error'):
            print(f"\n{item['content']}")
        elif item['type'] == 'dictoflist':
            print_table(item['content']['results'],
                        columns=item['content']['results'])
        elif item['type'] == 'listoflist':
            print_table(item['content'])
        elif item['type'] == 'list':
            for i in item:
                print(i)
