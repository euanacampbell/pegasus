import pymysql
import sqlparse
import yaml
import pyodbc
from rich.console import Console
from rich.table import Table
from rich import print
from pegasus.modules.generic.clipboard import Clipboard
from tabulate import tabulate
import os
import psutil


class sql:
    """Run a predetermined SQL command. Use 'sql help' for available commands."""

    def __init__(self):
        """Checks all contents exist in the yaml file"""

        with open('sql.yaml', 'r') as stream:
            config = yaml.safe_load(stream)

        config_requirements = ['connections',
                               'commands', 'combined_commands', 'better_tables', 'auto_format_queries']

        for section in config_requirements:
            try:
                setattr(self, section, config[section])
            except KeyError:
                raise Exception(f"\nmissing '{section}' from sql.yaml file\n")

    def __run__(self, params=None):

        if self.auto_format_queries:
            self.reformat_yaml()

        # check a sql command has been passed
        try:
            sql_command = params[0]
        except IndexError:
            raise Exception(
                "SQL command missing, type 'sql help' for available commands")

        sql_param = ' '.join(params[1:])

        # module commands
        command_dispatch = {
            'copy': self.copy_query,
            'view': self.view_queries,
            'help': self.help
        }

        if sql_command in command_dispatch:
            return command_dispatch[sql_command](sql_param)

        # runs either single or combi command
        if sql_command in self.commands:
            all_results = self.run_command(sql_command, sql_param)
        elif sql_command in self.combined_commands:
            all_results = []
            for command in self.combined_commands[sql_command]['commands']:
                all_results.append(command)
                for r in self.run_command(command, sql_param):
                    all_results.append(r)
        else:
            raise ValueError(f'Command not recognised: {sql_command}')
        return all_results

    def run_command(self, command, param):
        """Takes a given command/param and runs it"""

        query_details = self.commands[command]

        if query_details['parameter'] == True and len(param) == 0:
            raise ValueError('missing query parameter')

        all_results = []
        for query in query_details['queries']:

            sql_i = SQL_Conn()
            results = sql_i.run_query(
                self.connections[query_details['connection']], query, param)

            query_results = {
                'results': results['results'],
                'columns': results['columns']
            }
            all_results.append(query_results)

        return all_results
        # self.print_table(results['results'], results['columns'])

    def print_table(self, results, columns):
        """Displaying the query results"""

        if self.better_tables:
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

        return sqlparse.format(
            query, reindent=True, keyword_case='upper')

    def view_queries(self, command):

        queries = []

        if command not in self.commands and command not in self.combined_commands:
            raise Exception(
                f"Command '{command}' not recognised.")

        if command in self.commands:
            for query in self.commands[command]['queries']:
                query.replace('&p', "''")
                queries.append(self.format_sql(query))

        if command in self.combined_commands:
            sub_commands = [
                query for query in self.combined_commands[command]['commands']]
            for comm in sub_commands:
                queries.append(comm)
                for comm in self.commands[comm]['queries']:
                    comm.replace('&p', "''")
                    queries.append(self.format_sql(comm))

        return queries

    def copy_query(self, command):

        queries = self.commands[command]['queries']
        query_needed = 0
        if len(queries) != 1:
            self.view_queries(command)
            query_needed = int(input('\nquery to copy (number): '))-1

        query = self.format_sql(queries[query_needed])

        query = query.replace('&p', "''")
        Clipboard.add_to_clipboard(query)

        print('\ncopied to clipboard')

    def help(self, command):

        results_format = [{
            'results': [],
            'columns': ['command', 'description']
        }, f"\nUse 'sql copy' or 'sql view' for additional options."]

        sections = [self.commands, self.combined_commands]
        for section in sections:
            for command in section:
                desc = section[command]['description']

                results_format[0]['results'].append([command, desc])

        return results_format

    def reformat_yaml(self):
        """Converts any multi-line sql commands into a single line to make the config more readable"""

        with open('sql.yaml') as f:
            doc = yaml.safe_load(f)

        commands = doc['commands']
        for command in commands:
            new_queries = []
            for query in commands[command]['queries']:
                formatted_query = query.replace('\n', '')
                new_queries.append(formatted_query)

            doc['commands'][command]['queries'] = new_queries

        with open('sql.yaml', 'w') as f:
            yaml.dump(doc, f, width=2000)


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
                    params = [param for i in range(0, query.count('&p'))]
                    query = query.replace('&p', marker_lookup[self.type])

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

            self.connection.commit()

        return results
