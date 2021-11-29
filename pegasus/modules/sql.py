import pymysql
import sqlparse
import pyodbc
from rich.console import Console
from rich.table import Table
from rich import print
# from pegasus.modules.generic.clipboard import Clipboard
from tabulate import tabulate
# from pegasus.modules.format import format
import base64
import sqlite3
from pegasus.modules.setup.sql_config import *


class sql:
    """Run a predetermined SQL command. Use 'sql help' for available commands."""

    def __init__(self):
        """"""

        config = sql_config().load_config()

        config_requirements = ['connections',
                               'commands',
                               'queries',
                               'settings']

        # check correct sections exist in config
        for section in config_requirements:
            try:
                setattr(self, section, config[section])
            except KeyError:
                raise Exception(f"\nmissing '{section}' from db file\n")

    def __run__(self, params=None):

        # check a sql command has been passed
        try:
            sql_command = params[0]
        except IndexError:
            raise Exception(
                "SQL command missing, type 'sql help' for available commands")

        sql_param = ' '.join(params[1:])

        # module commands
        command_dispatch = {
            'view': self.view_queries,
            'help': self.help,
            'encrypt': self.encrypt,
            'delete_conn': sql_config().delete_conn,
            'add_conn': sql_config().update_conn,
            'add_query': sql_config().new_query,
            'delete_query': sql_config().delete_query,
            'add_command': sql_config().update_command,
            'delete_command': sql_config().delete_command,
        }

        if sql_command in command_dispatch:
            return command_dispatch[sql_command](sql_param)

        # runs either command or individual query
        if sql_command in self.commands or sql_command in self.queries:
            return self.run_command(sql_command, sql_param)
        else:
            raise ValueError(f'Command not recognised: {sql_command}')

    def run_command(self, command, param):
        """Takes a given command/param and runs it"""

        if command in self.commands:
            try:
                queries = self.commands[command]['query_order'].split(', ')
            except KeyError:
                return [f"'query_order' missing from db for command '{command}'."]

        elif command in self.queries:
            queries = [command]

        all_results = []

        border_started = False

        all_results.append(f"%start_row%")
        for index, query in enumerate(queries):

            query_details = self.queries[query]
            try:
                connection_details = self.connections[query_details['connection']]
            except KeyError:
                missing_connection = query_details['connection']
                all_results.append(
                    f"Connection '{missing_connection}' does not exist.")
                continue

            results = SQL_Conn().run_query(connection_details,
                                           query_details['query'], param)

            query_results = {
                'results': results['results'],
                'columns': results['columns']
            }

            prev_conn = self.queries[queries[index-1]]['connection']
            curr_conn = query_details['connection']

            if curr_conn != prev_conn:

                if border_started == True:
                    all_results.append(f"%end_border%")
                all_results.append(f"%start_border%")
                conn_str = query_details['connection']
                all_results.append(f"%header%{conn_str}")
                border_started = True
            elif index == 0:
                all_results.append(f"%start_border%")
                conn_str = query_details['connection']
                all_results.append(f"%header%{conn_str}")
                border_started = True

            if self.settings['two_columns']:
                all_results.append(f"%start_column%")

            all_results.append(query)
            all_results.append(query_results)

            if self.settings['two_columns']:
                all_results.append(f"%end_column%")

        if border_started == True:
            all_results.append(f"%end_border%")
        all_results.append(f"%end_row%")

        return all_results

    def subcommands(self):

        # pass back sub-commands (can be called directly without initial command), excludes module commands
        commands_keys = list(self.commands.keys())
        queries = list(self.queries.keys())

        sub_commands = commands_keys + queries

        return sub_commands

    def format_sql(self, query):

        return sqlparse.format(
            query, reindent=True, keyword_case='upper')

    def view_queries(self, command):

        queries = []

        if command not in self.commands and command not in self.queries:
            raise Exception(
                f"Command '{command}' not recognised.")

        if command in self.commands:
            for query in self.commands[command]['queries']:
                queries.append(self.format_sql(query.replace('&p', "''")))

        if command in self.queries:
            sub_commands = [
                query for query in self.queries[command]['query']]
            for comm in sub_commands:
                queries.append(comm)
                for comm in self.commands[comm]['queries']:
                    queries.append(self.format_sql(comm.replace('&p', "''")))

        return queries

    def help(self, command):

        commands = [command for command in self.commands]
        queries = [query for query in self.queries]

        return ['commands', commands, 'queries', queries]

    def encrypt(self, value):

        encrypted = base64.b64encode(value.encode("utf-8"))

        return str(encrypted)


class SQL_Conn:

    def get_connection(self, conn):
        self.type = conn['type']

        server = conn['server']
        database = conn['database']
        if self.type == 'mysql':
            self.get_tables = 'SHOW TABLES;'
            self.connection = pymysql.connect(host=conn['server'],
                                              user=conn['username'],
                                              password=base64.b64decode(
                                                  conn['password']).decode("utf-8"),
                                              database=conn['database'],
                                              cursorclass=pymysql.cursors.DictCursor)
        elif self.type == 'sqlserver':
            self.get_tables = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
            self.connection = pyodbc.connect(
                f'DRIVER=SQL Server; SERVER={server}; DATABASE={database};Trusted_Connection=yes;')
        elif self.type == 'azure':
            self.get_tables = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
            username = conn['username']
            password = base64.b64decode(conn['password']).decode("utf-8")
            driver = '{ODBC Driver 17 for SQL Server}'
            connection = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={{' + \
                password + '};Authentication=ActiveDirectoryPassword'
            self.connection = pyodbc.connect(connection)
            self.connection.add_output_converter(-155, str)
        else:
            raise Exception(f"type {self.type} not recognised")

    def run_query(self, conn, query, param=None):
        results = {}
        self.get_connection(conn)

        with self.connection:
            with self.connection.cursor() as cursor:
                if '&p' in query:
                    if not param:
                        raise ValueError('Missing query parameter')

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

                # tables = cursor.execute(self.get_tables).fetchall()
                # results['tables'] = [table[2] for table in tables if table[1]=='dbo']

            self.connection.commit()

        return results


class sql_config:

    def __init__(self):
        self.db = Database()

    def load_config(self):

        config = {
            'settings': self.get_settings(),
            'connections': self.get_all_connections(),
            'commands': self.get_commands(),
            'queries': self.get_queries(),
        }

        return config

    def new_query(self, query_command, connection, query):

        self.db.run('add_query', params=(query_command, connection, query))

    def delete_query(self, query_name):

        self.db.run('delete_query', params=(query_name))
        self.db.run('delete_query_from_command', params=(query_name))

    def update_settings(self, enabled_settings):

        config = self.load_config()

        skip = ['queries', 'commands', 'connections']

        for item in config['settings']:
            if item not in skip:
                if item in enabled_settings:
                    config['settings'][item] = True
                else:
                    config['settings'][item] = False

    def delete_conn(self, conn, check_queries=True):

        # check_queries is used to check if any queries are using this connection
        if check_queries:
            queries = self.db.run('get_all_queries')
            for query in queries:
                if query[2] == conn:
                    raise Exception(
                        'Connection is still in use, remove from all queries before trying again.')

        self.db.run('delete_connection', params=conn)

        return f'connection {conn} deleted'

    def update_conn(self, connection):

        self.delete_conn(connection['name'], check_queries=False)

        connection['password'] = base64.b64encode(
            connection['password'].encode("utf-8"))

        self.db.run('add_connection', params=(
            connection['name'], connection['server'], connection['database'], connection['type'], connection['username'], connection['password']))

    def get_all_connections(self):

        all_conns = self.db.run('get_all_connections')

        conns = {}

        for conn in all_conns:
            conns[conn[1]] = {
                'server': conn[2],
                'database': conn[3],
                'type': conn[4],
                'username': conn[5],
                'password': conn[6]
            }

        return conns

    def get_settings(self):

        settings = self.db.run('get_all_settings')

        return_settings = {}

        for setting in settings:
            if setting[2].lower() == 'false':
                value = False
            elif setting[2].lower() == 'true':
                value = True
            else:
                value = setting[2]

            return_settings[setting[1]] = value

        return return_settings

    def get_commands(self):
        commands = self.db.run('get_all_commands')

        unique_commands = list(set([com[1] for com in commands]))

        return_commands = {}

        for unique_command in unique_commands:
            queries = []
            for command in commands:
                if command[1] == unique_command:
                    queries.append(command[2])
            return_commands[unique_command] = {
                'queries': queries,
                'query_order': ', '.join(queries)
            }

        return return_commands

    def get_queries(self):

        queries = self.db.run('get_all_queries')

        return_queries = {}

        for query in queries:
            return_queries[query[1]] = {
                'connection': query[2],
                'query': query[3],
            }

        return return_queries

    def update_command(self, command_name, queries, query_order):

        query_order = query_order.split(", ")

        query_order = [query.strip()
                       for query in query_order if query.strip() in queries]
        for query in queries:
            if query not in query_order:
                query_order.append(query)

        self.db.run('delete_command', params=command_name)

        for count, query in enumerate(query_order):
            self.db.run('add_command', params=(command_name, query, count))

    def delete_command(self, command_name):

        self.db.run('delete_command', params=(command_name))


class Database:

    def __init__(self):

        try:
            self.run_query(
                f"SELECT * FROM Connections", ())
        except:
            print('no sql config setup, building now.')
            self.setup_db()

    def run(self, query_name, params=()):

        query = QUERIES_LOOKUP[query_name]

        if type(params) == str:
            params = tuple([params])

        return self.run_query(query, params)

    def run_query(self, query, params):

        connection = sqlite3.connect("sql.db")
        cursor = connection.cursor()

        rows = cursor.execute(query, params).fetchall()

        connection.commit()

        return rows

    def setup_db(self):

        for query in SETUP_QUERIES:
            self.run_query(query, ())


if __name__ == "__main__":

    sql = sql_config()

    print(sql.load_config())
