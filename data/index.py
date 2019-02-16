import sqlite3
from config import TABLES, DATABASE

class Database:
    def __init__ (self):
        self.connection = None
        self.has_connection = False

        cursor = self.get_cursor()

        for table_name in TABLES:
            table_data = TABLES[table_name]
            string_query = (self.create_table_string(table_data, table_name))
            cursor.execute(string_query)

        self.commit_connection()
        self.close_connection()
    '''
        Returns a table string for data
    '''
    def create_table_string(self, table_data, table_name):
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
    def get_cursor(self):
        if (not self.connection or not self.has_connection):
            self.connection = sqlite3.connect(DATABASE)
            self.has_connection = True
        return self.connection.cursor()

    '''
        Saves whatever data has with the current connection
    '''
    def commit_connection(self):
        if (self.has_connection):
            self.connection.commit()
            return False
        return True

    '''
        Closes the connection
    '''
    def close_connection(self):
        if (self.has_connection):
            self.connection.close()
            self.has_connection = False
            return False
        return True
