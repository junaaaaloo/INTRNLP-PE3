import sqlite3
from config import TABLES, DATABASE

# Global Variables
connection = None
has_connection = False

# Global Methods

'''
    Returns a table string for data
'''
def create_table_string(table_data, table_name):
    message = "CREATE TABLE IF NOT EXISTS {} ".format(table_name)

    column_count = 0
    message += "("
    for column_name in table_data['columns']:
        column_data = table_data['columns'][column_name]
        message += "{} {}{}".format(
            column_name, column_data['type'], (" PRIMARY KEY" if 'primary_key' in column_data else ""))
        column_count += 1
        if (column_count != len(table_data['columns'])):
            message += ", "

    message += ")"

    return message

'''
    Returns a cursor of the connection to be used
'''
def get_cursor():
    global connection, has_connection
    if (not connection or not open_connection):
        connection = sqlite3.connect(DATABASE)
        has_connection = True
    return connection.cursor()

'''
    Saves whatever data has with the current connection
'''
def commit_connection():
    global connection, has_connection
    if (has_connection):
        connection.commit()

'''
    Closes the connection
'''
def close_connection():
    global connection, has_connection
    if (has_connection):
        connection.close()
        has_connection = False

'''
    Initializes the database with all the tables
'''
def initialize_db():
    cursor = get_cursor()

    for table_name in TABLES:
        table_data = TABLES[table_name]
        string_query = (create_table_string(table_data, table_name))
        cursor.execute(string_query)

    commit_connection()
    close_connection()


initialize_db()
