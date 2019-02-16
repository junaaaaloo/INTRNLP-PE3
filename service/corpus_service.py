from queries import QueryBuilder

class CorpusItem:
    def __init__ (self, id, name, count):
        self.id = id
        self.name = name
        self.count = count
    

class CorpusService:
    def __init__ (self, database):
        self.database = database
    
    def add (self, corpus):
        cursor = self.database.get_cursor()

        cursor.execute(QueryBuilder.insert(table, ["name", "count"])


    def get (self, filters):
        cursor = self.database.get_cursor()


    