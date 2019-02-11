class DatasetCacher:

    DEFAULT_STORAGE_LOCATION = '.'

    def __init__(self, dataset_name, storage_location=None, verbose=False):
        if not storage_location:
            storage_location = self.DEFAULT_STORAGE_LOCATION

        self.storage_location = storage_location
        self.dataset_name = dataset_name
        self.verbose = verbose

    def cache_dataset(self, dataset):
        raise NotImplementedError

    def cache(self, *args):
        """ Alias for `cache_dataset`. """

        self.cache_dataset(*args)
