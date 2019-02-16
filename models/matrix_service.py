TABLE_NAME = 'confusion_matrix'
TABLE_DATA = {
    'columns': {
        'id': {"type": 'INTEGER', "primary_key": True, "autoincrement": True},
        'mistake': {"type": 'TEXT'},
        'correct': {"type": 'TEXT'},
        'count': {"type": 'INTEGER'}
    }
}

def add (cursor, values):
    data = [] 
    for value in values:
        data.append([value.id, value.mistake, value.correct, value.count])

    cursor.executemany('INSERT INTO {} VALUES (?,?,?,?,?)'.format(TABLE_NAME), data)
    
    # Do this instead
    t = ('RHAT',)
    c.execute('SELECT * FROM stocks WHERE symbol=?', t)
    print c.fetchone()

    # Larger example that inserts many records at a time
    purchases = [
                    ('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                    ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                    ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
                ]
    


def edit (cursor, id, matrix):
    pass

def delete (cursor, id):
    pass
    
def get (cursor, id, conditions = None):
    pass
