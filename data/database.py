import sqlite3

tables = {
    'vocabulary': {
        'columns': {
            'id': { "type": 'INTEGER', "primary_key": True },
            'name': { "type": 'TEXT' },
            'count': { "type": 'INTEGER' }
        }
    },
    'matrix': {
        'columns': {
            'id': { "type": 'INTEGER', "primary_key": True },
            'mistake': { "type": 'TEXT' },
            'correct': { "type": 'TEXT'},
            'count': { "type": 'INTEGER' }
        }
    }
}

def create_table_string (table_data, table_name):
    message = "CREATE TABLE {} ".format(table_name)

    column_count = 0
    message += "("
    for column_name in table_data['columns']:
        column_data = table_data['columns'][column_name]
        message += "{} {}{}".format(column_name, column_data['type'], (" PRIMARY KEY" if 'primary_key' in column_data else ""))
        column_count += 1
        if (column_count != len(table_data['columns'])):
            message += ", "

    message += ")"

    return message

def create_database ():
    connection = sqlite3.connect("sqlite3.db")
    cursor = conenction.cursor()
    
    for table_name in tables:
        table_data = tables[table_name]
        string_query = (create_table_string(table_data, table_name))

create_database() 

# sqlite_file = 'gram.sqlite'    # name of the sqlite database file
# table_name1 = 'my_table_1'  # name of the table to be created
# table_name2 = 'my_table_2'  # name of the table to be created
# new_field = 'my_1st_column' # name of the column
# field_type = 'INTEGER'  # column data type

# # Connecting to the database file
# c = conn.cursor()

# # Creating a new SQLite table with 1 column
# c.execute('CREATE TABLE {tn} ({nf} {ft})'\
#         .format(tn=table_name1, nf=new_field, ft=field_type))

# # Creating a second table with 1 column and set it as PRIMARY KEY
# # note that PRIMARY KEY column must consist of unique values!
# c.execute('CREATE TABLE {tn} ({nf} {ft} PRIMARY KEY)'\
#         .format(tn=table_name2, nf=new_field, ft=field_type))

# # Committing changes and closing the connection to the database file
# conn.commit()
# conn.close()