import os
from .dataset_cacher import DatasetCacher
from ..database_adapters.sqlite import SQLite


class SQLiteDatasetCacher(DatasetCacher):

    DEFAULT_DATABASE_NAME = 'dataset_cacher.sqlite'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.database_location = os.path.join(self.storage_location, self.DEFAULT_DATABASE_NAME)
        self.connection = SQLite().connect(self.database_location)
        self.cursor = self.connection.cursor()

        self.__ensure_dataset_table_exists__()

    def __commit__(self):
        self.connection.commit()

    def __close__(self):
        self.connection.close()

    def __ensure_dataset_table_exists__(self):
        if not self.__table_exists__(self.dataset_name):
            self.__create_dataset_table__(self.dataset_name)

    def __create_dataset_table__(self, table_name):
        self.cursor.execute(f'CREATE TABLE {table_name} (x TENSOR NOT NULL, y TENSOR NOT NULL, identifier TEXT NOT NULL)')

    def __table_exists__(self, table_name):
        selection = self.cursor.execute(f'SELECT count(*) FROM sqlite_master WHERE type="table" AND name="{table_name}"')
        return selection.fetchone()[0] == 1

    def __cache_sample__(self, sample, commit=True):
        x, y, id = sample
        sql = f'INSERT INTO {self.dataset_name} (x, y, identifier) VALUES (?, ?, ?)'

        if self.verbose:
            print(sql)

        self.cursor.execute(sql, (x, y, id))

        if commit:
            self.__commit__()
            self.__close__()

    def cache_dataset(self, dataset):
        for sample in dataset:
            self.__cache_sample__(sample, commit=False)
            self.__commit__()

        self.__close__()
