import sqlite3

class SqlController:

    def __init__(self):
        pass

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            # print(sqlite3.version)
        except sqlite3.Error as e:
            print(e)

    
    def create_table(self, table_name, column_names=[]):
        if len(column_names)==0:
            print('no column names provided')
            return()


        query = f""" CREATE TABLE IF NOT EXISTS {table_name} (
                                        {table_name}_id integer PRIMARY KEY AUTOINCREMENT
                                        """

        for column in column_names:
            query += f""",[{column}] text
                      """      

        query += ");"

        self.run_query(query)

        return()

    def close_connection(self):

        if self.conn:
            self.conn.close()

    def run_query(self, query):
        try:
            c = self.conn.cursor()
            c.execute(query)
            self.conn.commit()
            return(c)
        except sqlite3.Error as e:
            print(e)
    
    def drop_table(self, table_name):
        query = f"DROP TABLE {table_name}"

        self.run_query(query)

        return()