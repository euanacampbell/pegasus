
SETUP_QUERIES = [
    "CREATE TABLE Settings(setting_id INTEGER PRIMARY KEY, setting TEXT, value TEXT)",
    "INSERT INTO Settings VALUES (NULL, 'better_tables','true')",
    "INSERT INTO Settings VALUES (NULL, 'settings','false')",
    "INSERT INTO Settings VALUES (NULL, 'two_columns','false')",
    "CREATE TABLE Queries(query_id INTEGER PRIMARY KEY, name TEXT, connection_id TEXT, query TEXT)",
    "CREATE TABLE Commands(command_id INTEGER PRIMARY KEY, name TEXT, query_id TEXT, priority INTEGER)",
    "CREATE TABLE Connections(connection_id INTEGER PRIMARY KEY, name TEXT, server TEXT, database TEXT, type TEXT, username TEXT, password BLOB)",
]

QUERIES_LOOKUP = {
    'add_query': "INSERT INTO Queries VALUES (NULL,?,?,?)",
    'get_all_queries': "SELECT * FROM Queries",
    'delete_query': "DELETE FROM Queries WHERE name = ?",
    'add_connection': "INSERT INTO Connections VALUES (NULL, ?,?,?,?,?,?)",
    'get_all_connections': "SELECT * FROM Connections",
    'delete_connection': "DELETE FROM Connections WHERE name=?",
    'add_command': "INSERT INTO Commands VALUES (NULL, ?,?, ?)",
    'get_all_commands': "SELECT * FROM Commands",
    'delete_command': "DELETE FROM Commands WHERE name=?",
    'delete_query_from_command': "DELETE FROM Commands WHERE query_id=?",
    'get_all_settings': "SELECT * FROM Settings"
}
