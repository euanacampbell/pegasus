import sqlite3
from sqlite3 import Error
from tabulate import tabulate

try:
    from modules.generic.clipboard import Clipboard
except:
    from generic.clipboard import Clipboard

try:
    from modules.generic.SqlController import SqlController
except:
    from generic.SqlController import SqlController

class sql:
    """Generic class for handling various SQL tasks"""

    def __init__(self, config=None):
        self.config=config

        self.sql = SqlController()

    def __run__(self, command):
        self.create_connection("C:/Users/euan.campbell/projects/pegasus/assets/SQL/main.db")
        
        commands = ['load_clipboard', 'select', 'exit', 'print_table']

        if command not in commands:
            print('command not recognised')
        
        elif command == 'load_clipboard':

            table_name = input('\ntable name: ')
            
            if table_name=='exit':
                return()

            self.clipboard_to_db(table_name)

            print(f'successfully created {table_name}')
        elif command == 'print_table':
            table = input('table name: ')
            self.select(f"SELECT * FROM {table};", print_results=True)
        elif command == 'select':
            query = input('query: ')
            self.select(query, print_results=True)

    

    def insert_list(self, table, input_list):
        
        if not isinstance(input_list[0], list):
            list_of_lists=[input_list]
        else:
            list_of_lists=input_list
        
        for row in list_of_lists:
            query = f""" INSERT INTO {table} VALUES("""

            # get new id and add to row
            new_id = int(self.select(f'SELECT MAX({table}_id) FROM {table}')[0][0] or 0)+1
            row.insert(0,new_id)
            
            # add each column to VALUES
            for column in row:
                query += f"'{column}',"
            
            query = query[:-1] + ')' # remove final comma and add closing bracket

            self.run_query(query)

        return()

    def select(self, query, print_results=False):

        cur = self.run_query(query)
        rows = cur.fetchall()

        column_names = [d[0] for d in cur.description]

        if print_results:
            self.print_results(rows, column_names)

        return(rows)


    
    def csv_to_db(self, path_to_file, has_header=False):
        pass

    def clipboard_to_db(self, table_name):

        clipboard = Clipboard.get_clipboard().splitlines()
        if '\t' in clipboard[0]:
            master = [row.split('\t') for row in clipboard]
        if '\n' in clipboard[0]:
            master = [row.split('\n') for row in clipboard]

        columns=master[0]
        data=master[1:]

        self.create_table(table_name, column_names=columns)

        self.insert_list(table_name, data)
        
        self.close_connection()

    def print_results(self, results, columns):
        
        print(tabulate(results, headers=columns, tablefmt="pretty"))

if __name__ == '__main__':

    db = sql()

    # db.drop_table('test')

    # db.create_table('test', column_names=['name', 'email', 'phone'])

    # db.insert_list('test', ['euan campbell', 'hello@euan.app', '07977055775'])
    db.select("SELECT * FROM historic_a LIMIT 5;", print_results=True)

    db.close_connection()


"""
Tools:
- db from clipboard
- db from csv file
- db from SQL server
- query db
"""