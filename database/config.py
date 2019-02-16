DATABASE = "sqlite3.db"
TABLES = {
    'vocabulary': {
        'columns': {
            'id': {"type": 'INTEGER', "primary_key": True, "autoincrement": True},
            'name': {"type": 'TEXT'},
            'count': {"type": 'INTEGER'}
        }
    },
    'confusion_matrix': {
        'columns': {
            'id': {"type": 'INTEGER', "primary_key": True, "autoincrement": True},
            'mistake': {"type": 'TEXT'},
            'correct': {"type": 'TEXT'},
            'count': {"type": 'INTEGER'}
        }
    }
}

CORPUS_DIRECTORY = "corpus/"
