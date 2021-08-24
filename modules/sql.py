import pymysql
import sqlparse
import yaml
import pyodbc
from rich.console import Console
from rich.table import Table
from rich import print
from modules.generic.clipboard import Clipboard
from tabulate import tabulate
import os
import psutil


class sql:
    """Run a predetermined SQL command"""

    def __init__(self):

        pass
    
    def setup(self):
        with open('sql.yaml', 'r') as stream:
            config = yaml.safe_load(stream)

        try:
            self.connections = config['connections']
        except KeyError:
            print('missing rich_tables value in sql.yaml file')

        try:
            self.commands = config['commands']
        except KeyError:
            print('missing rich_tables value in sql.yaml file')
            
        try:
            self.combi_commands = config['combined_commands']
        except KeyError:
            print('missing rich_tables value in sql.yaml file')

        try:
            self.rich_tables = config['rich_tables']
        except KeyError:
            print('missing rich_tables value in sql.yaml file')

    def __run__(self, params=None):
        
        self.setup()

        # check a sql command has been passed
        try:
            sql_command = params[0]
        except IndexError:
            print("missing sql command, type 'sql help' for options")
            return

        sql_param = ' '.join(params[1:])

        # module commands
        command_dispatch = {
            'copy': self.copy_query,
            'view': self.view_queries,
            'help': self.help
        }

        if sql_command in command_dispatch:
            command_dispatch[sql_command](sql_param)
            return

        # runs either single or combi command
        if sql_command in self.commands:
            self.run_command(sql_command, sql_param)
        elif sql_command in self.combi_commands:
            for command in self.combi_commands[sql_command]['commands']:
                print(f"\n{command}")
                self.run_command(command, sql_param)
        else:
            print('command not recognised')
            return

    def run_command(self, command, param):

        query_details = self.commands[command]

        if query_details['parameter'] == True and len(param) == 0:
            raise Exception('missing query parameter')

        conn_details = self.connections[query_details['connection']]
        for query in query_details['queries']:

            sql_i = SQL_Conn()
            results = sql_i.run_query(conn_details, query, param)

            formatted = ', '.join(results['tables'])

            # print(f"\n[bold]{formatted}[/bold]")
            self.print_table(results['results'], results['columns'])

    def print_table(self, results, columns):

        if self.rich_tables:
            console = Console()
            table = Table(show_header=True, header_style="bold")

            table.row_styles = ["none", "dim"]

            for col in columns:
                table.add_column(col)

            for row in results:
                table.add_row(*row)

            console.print(table)
        else:
            print(tabulate(results, headers=columns, tablefmt="pretty"))

    def format_sql(self, query):

        formatted = sqlparse.format(
            query, reindent=True, keyword_case='upper')

        return formatted

    def view_queries(self, command):
        queries = self.commands[command]['queries']

        for index, query in enumerate(queries):
            print(f'\n{index+1}')
            try:
                query = query.replace('&p', "''")
                print(self.format_sql(query))
            except:
                print('(issue formatting this one)')
                query = query.replace('&p', "''")
                print(query)

    def copy_query(self, command):

        queries = self.commands[command]['queries']

        if len(queries) == 1:
            query = self.format_sql(queries[0])
            query = query.replace('&p', "''")
        else:
            self.view_queries(command)
            number = int(input('\nquery to copy (number): '))
            query = self.format_sql(queries[number-1])
        query = query.replace('&p', "''")
        Clipboard.add_to_clipboard(query)

        print('copied to clipboard')

    def help(self, command):

        print("\nsql commands")
        for command in self.commands:
            desc = self.commands[command]['description']
            print(f"{command} : {desc}")

        print("\ncombined sql commands")
        for command in self.combi_commands:
            desc = self.combi_commands[command]['description']
            print(f"{command} : {desc}")

        print(
            f"\n(type 'copy' or 'view' after your sql command for additional options)")

        return
    
    def reformat_yaml(self):
        """Converts any multi-line sql commands into a single line to make the config more readable"""

        with open('sql.yaml') as f:
            doc = yaml.load(f)

        commands = doc['commands']
        for command in commands:
            for query in command['queries']:
                formatted_query = query.replace('\n','')
                commands[command][]

        with open('sql.yaml', 'w') as f:
            yaml.dump(doc, f)


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
                        'mysql': '%s',
                        'azure': '?'
                    }

                    # get number of markers a
                    marker_count = query.count('&p')

                    # insert correct marker
                    query = query.replace('&p', marker_lookup[self.type])

                    # create parameter for every marker (allows for multiple markers)
                    params = [param for i in range(0, marker_count)]

                    cursor.execute(query, params)
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
        return set(tables)
