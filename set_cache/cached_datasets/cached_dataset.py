import os
import torch.utils.data


class CachedDataset(torch.utils.data.Dataset):

    DEFAULT_STORAGE_LOCATION = 'tmp'

    def __init__(self, dataset_name, storage_location=None):
        if not storage_location:
            storage_location = self.DEFAULT_STORAGE_LOCATION

        self.storage_location = storage_location
        self.dataset_name = dataset_name

    def __len__(self):
        return len(self.ids)

    def __getitem__(self, index):
        ids = self.ids[index]

        # At this point `ids` could be a list of IDs or one ID. Ensure it is
        # a list of IDs *in any case* to simplify further processing.
        if not isinstance(ids, list):
            ids = [ids]

        samples = self.__load_samples__(ids)

        # Don't return a list of samples if only a specifc sample was requested.
        if len(ids) == 1:
            return samples[0]

        return samples
