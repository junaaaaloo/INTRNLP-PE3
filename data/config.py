DATABASE = "sqlite3.db"
TABLES = {
    'corpus': {
        'columns': {
            'id': {"type": 'INTEGER', "primary_key": True},
            'name': {"type": 'TEXT'},
            'count': {"type": 'INTEGER'}
        }
    },
    'confusion_matrix': {
        'columns': {
            'id': {"type": 'INTEGER', "primary_key": True},
            'mistake': {"type": 'TEXT'},
            'correct': {"type": 'TEXT'},
            'count': {"type": 'INTEGER'}
        }
    }
}

CORPUS_DIRECTORY = "corpus/"
