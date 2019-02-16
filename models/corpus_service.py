TABLE_NAME = 'vocabulary'
TABLE_DATA = {
    'columns': {
        'id': {"type": 'INTEGER', "primary_key": True, "autoincrement": True},
        'name': {"type": 'TEXT'},
        'count': {"type": 'INTEGER'}
    }
}

def add (cursor, word):
    cursor.execute("INSERT")

def edit (cursor, id, matrix):
    pass

def delete (cursor, id):
    pass
    
def get (cursor, conditions = None):
    pass

