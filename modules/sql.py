import pymysql
import sqlparse
import yaml
import pyodbc
from rich.console import Console
from rich.table import Table
from rich import print
from modules.generic.clipboard import Clipboard


class sql:
    """Run a predetermined SQL command"""

    def __init__(self):

        with open('sql.yaml', 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise Exception(exc)

        self.connections = config['connections']
        self.commands = config['sql_commands']

    def __run__(self, params=None):

        # check a sql command has been passed
        try:
            sql_command = params[0]
        except IndexError:
            print("missing sql command, type 'sql help' for options")
            return()

        if sql_command == 'help':
            for command in self.commands:
                desc = self.commands[command]['description']
                print(f"{command} : {desc}")
            print(
                f"\n(type 'copy' or 'view' after your sql command for additional options)")
            return()

        # query details for query and connection details for where to run it
        try:
            query_details = self.commands[sql_command]
        except:
            print("invalid sql command, type 'sql help' for available commands")
            return()
        conn_details = self.connections[query_details['connection']]

        sql_param = ' '.join(params[1:])

        command_dispatch = {
            'copy': self.copy_query,
            'view': self.view_queries

        }

        if sql_param in command_dispatch:
            command_dispatch[sql_param](sql_command)
            return()

        if query_details['parameter'] == True and len(sql_param) == 0:
            raise Exception('missing query parameter')

        for query in query_details['queries']:

            sql_i = SQL_Conn()
            results = sql_i.run_query(conn_details, query, sql_param)

            formatted = ', '.join(results['tables'])

            # print(f'\ntables: {formatted}')
            print(f"\n[bold]{formatted}[/bold]")
            self.print_table(results['results'], results['columns'])

    def print_table(self, results, columns):

        console = Console()
        table = Table(show_header=True, header_style="bold")

        table.row_styles = ["none", "dim"]

        for col in columns:
            table.add_column(col)

        for row in results:
            table.add_row(*row)

        console.print(table)

    def format_sql(self, query):

        formatted = sqlparse.format(
            query, reindent=True, keyword_case='upper')

        return formatted

    def view_queries(self, command):
        queries = self.commands[command]['queries']

        for index, query in enumerate(queries):
            print(f'\n{index+1}')
            try:
                print(self.format_sql(query))
            except:
                print('(issue formatting this one)')
                print(query)

    def copy_query(self, command):

        queries = self.commands[command]['queries']

        if len(queries) == 1:
            Clipboard.add_to_clipboard(self.format_sql(queries[0]))
        else:
            self.view_queries(command)
            number = int(input('\nquery to copy (number): '))
            Clipboard.add_to_clipboard(self.format_sql(queries[number-1]))

        print('copied to clipboard')


class SQL_Conn:

    def get_connection(self, conn):
        self.type = conn['type']

        server = conn['server']
        database = conn['database']
        if self.type == 'mysql':
            self.connection = pymysql.connect(host=conn['server'],
                                              user=conn['username'],
                                              password=conn['password'],
                                              database=conn['database'],
                                              cursorclass=pymysql.cursors.DictCursor)
        elif self.type == 'sqlserver':
            self.connection = pyodbc.connect(
                f'DRIVER=SQL Server; SERVER={server}; DATABASE={database};Trusted_Connection=yes;')
        elif self.type == 'azure':
            username = conn['username']
            password = conn['password']
            self.connection = pyodbc.connect(
                f'DRIVER=SQL Server; SERVER={server}; DATABASE={database}; UID={username}; PWD={password}')
        else:
            raise Exception(f"type {self.type} not recognised")

    def run_query(self, conn, query, param=None):

        results = {}

        self.get_connection(conn)

        with self.connection:
            with self.connection.cursor() as cursor:
                if param:

                    marker_lookup = {
                        'sqlserver': '?',
                        'mysql': '%s'
                    }

                    query = query.replace('&p', marker_lookup[self.type])

                    cursor.execute(query, param)
                else:
                    cursor.execute(query)

                content = cursor.fetchall()
                if self.type == 'mysql':

                    string_dict = []

                    for row in content:
                        keys_values = row.items()
                        string_dict.append({str(key): str(value)
                                            for key, value in keys_values})

                    results['results'] = [list(i.values())
                                          for i in string_dict]

                else:
                    new_content = []
                    for res in content:
                        new_row = [str(i) for i in res]
                        new_content.append(new_row)

                    results['results'] = new_content

                results['columns'] = [i[0] for i in cursor.description]
                results['tables'] = self.tables_used(query)

            self.connection.commit()

        return results

    def tables_used(self, query):

        query_list = [word for word in query.split(' ') if word]

        tables = []

        for index, word in enumerate(query_list):

            if word in ('FROM', 'JOIN', 'from', 'join') and query_list[index+1] not in tables:

                table = query_list[index+1].lower()
                formatted_table = table.split('.')[-1]

                remove_characters = ['(', ')', '[', ']']

                for char in remove_characters:
                    formatted_table = formatted_table.replace(char, "")

                tables.append(formatted_table)
        return(set(tables))
