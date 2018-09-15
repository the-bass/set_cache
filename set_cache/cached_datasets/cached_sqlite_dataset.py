import os
from .cached_dataset import CachedDataset
from ..database_adapters.sqlite import SQLite


class CachedSQLiteDataset(CachedDataset):

    def __init__(self, dataset_name, ids, storage_location=None):
        self.ids = ids

        super().__init__(dataset_name, storage_location=storage_location)

        self.database_location = os.path.join(self.storage_location, 'dataset_cacher.sqlite')
        self.connection = SQLite().connect(self.database_location)
        self.cursor = self.connection.cursor()

    def __load_samples__(self, ids):
        ids_sql = ", ".join([str(id) for id in ids])
        selection = self.cursor.execute(f'SELECT x, y, identifier FROM {self.dataset_name} WHERE RowID IN ({ids_sql})')
        return selection.fetchall()

    @classmethod
    def load_dataset(cls, dataset_name, storage_location=None, limit=None):
        storage_location = storage_location if storage_location else cls.DEFAULT_STORAGE_LOCATION

        database_location = os.path.join(storage_location, 'dataset_cacher.sqlite')
        connection = SQLite().connect(database_location)
        cursor = connection.cursor()

        id_selection_query = f'SELECT RowID FROM {dataset_name}'
        if limit:
            id_selection_query += f' LIMIT {limit}'

        id_selection = cursor.execute(id_selection_query)
        ids = [row[0] for row in id_selection.fetchall()]

        return cls(dataset_name, ids, storage_location=storage_location)
