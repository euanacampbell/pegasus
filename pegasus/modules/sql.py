import pymysql
import sqlparse
import yaml
import pyodbc
from rich.console import Console
from rich.table import Table
from rich import print
from pegasus.modules.generic.clipboard import Clipboard
from tabulate import tabulate
from pegasus.modules.format import format


class sql:
    """Run a predetermined SQL command. Use 'sql help' for available commands."""

    def __init__(self):
        """Checks all contents exist in the yaml file"""

        config = sql_config().load_config()

        config_requirements = ['connections',
                               'commands',
                               'queries',
                               'better_tables',
                               'auto_format_queries']

        # check correct sections exist in config
        for section in config_requirements:
            try:
                setattr(self, section, config[section])
            except KeyError:
                raise Exception(f"\nmissing '{section}' from sql.yaml file\n")

    def __run__(self, params=None):

        if self.auto_format_queries:
            sql_config().reformat_yaml()

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

        # runs either command or individual query
        if sql_command in self.commands:
            return self.run_command(sql_command, sql_param)
        if sql_command in self.queries:
            return self.run_command(sql_command, sql_param)
        else:
            raise ValueError(f'Command not recognised: {sql_command}')

    def run_command(self, command, param):
        """Takes a given command/param and runs it"""

        if command in self.commands:
            queries = self.commands[command]['queries']
        elif command in self.queries:
            queries = [command]

        all_results = []
        for query in queries:

            query_details = self.queries[query]

            if query_details['connection'] not in self.connections:
                all_results.append(f'ERROR: Invalid connection for {query}')
                continue
            else:
                connection_details = self.connections[query_details['connection']]

            results = SQL_Conn().run_query(connection_details,
                                           query_details['query'], param)

            query_results = {
                'results': results['results'],
                'columns': results['columns']
            }
            all_results.append(query_results)

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

        if command not in self.commands and command not in self.combined_commands:
            raise Exception(
                f"Command '{command}' not recognised.")

        if command in self.commands:
            for query in self.commands[command]['queries']:
                queries.append(self.format_sql(query.replace('&p', "''")))

        if command in self.combined_commands:
            sub_commands = [
                query for query in self.combined_commands[command]['commands']]
            for comm in sub_commands:
                queries.append(comm)
                for comm in self.commands[comm]['queries']:
                    queries.append(self.format_sql(comm.replace('&p', "''")))

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
        }, f"\nUse 'sql copy' or 'sql view' for additional options.\nVisit /sqlsetup to modify the configuration"]

        sections = [self.commands, self.queries]
        for section in sections:
            for command in section:
                try:
                    desc = section[command]['description']
                except:
                    desc = ''

                results_format[0]['results'].append([command, desc])

        return results_format


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

            self.connection.commit()

        return results


class sql_config:

    def __init__(self):
        pass

    def load_config(self):
        with open('configs/sql.yaml', 'r') as stream:
            config = yaml.safe_load(stream)

        return config

    def update_config(self, new_config):

        with open('configs/sql.yaml', 'w') as f:
            yaml.dump(new_config, f, width=2000)

    def reformat_yaml(self):
        """Converts any multi-line sql commands into a single line to make the config more readable"""

        doc = self.load_config()

        queries = doc['queries']
        for query in queries:

            formatted_query = query.replace('\n', '')

            doc['queries'][query]['query'] = formatted_query

        self.update_config(doc)

    def new_query(self, query_command, connection, query):

        config = self.load_config()

        config['queries'][query_command] = {
            'query': query,
            'connection': connection
        }

        self.update_config(config)

    def delete_query(self, query):

        config = self.load_config()

        del config['queries'][query]

        self.update_config(config)

    def update_settings(self, enabled_settings):

        config = self.load_config()

        skip = ['queries', 'commands', 'connections']

        for item in config:
            if item not in skip:
                if item in enabled_settings:
                    config[item] = True
                else:
                    config[item] = False

        self.update_config(config)

    def delete_conn(self, conn):

        config = self.load_config()

        del config['connections'][conn]

        self.update_config(config)

    def update_conn(self, connection_name, connection_details):

        config = self.load_config()

        config['connections'][connection_name] = connection_details

        self.update_config(config)

    def update_command(self, command_name, queries):

        config = self.load_config()

        config['commands'][command_name] = {'queries': queries}

        self.update_config(config)

    def delete_command(self, command_name):

        config = self.load_config()

        del config['commands'][command_name]

        self.update_config(config)
