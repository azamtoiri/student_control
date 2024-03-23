class LazyDatabase:
    def __init__(self, database):
        self._database = None
        self._database_class = database

    @property
    def database(self):
        if self._database is None:
            self._database = self._database_class()
        return self._database
