import unittest
import torch
import os
import shutil
import torch_testing as tt
from set_cache import SQLiteDatasetCacher, CachedSQLiteDataset


class TestSQLiteDatasetCacher(unittest.TestCase):

    def setUp(self):
        self.dataset_name = 'audio_samples'
        self.storage_location = os.path.join('tests', 'tmp')

        if not os.path.exists(self.storage_location):
            os.makedirs(self.storage_location)

        self.dataset_cacher = SQLiteDatasetCacher(
            dataset_name=self.dataset_name,
            storage_location=self.storage_location)

    def tearDown(self):
        shutil.rmtree(self.storage_location)

    def test_cache_with_identifier(self):
        dataset = [
            (torch.ones(2, 3, 4).float(), torch.ones(1, 1).float(), 'sfk7fsjk/.mkfsd'),
            (torch.zeros(2, 3, 4).float(), torch.zeros(1, 1).float(), '41234')]
        self.dataset_cacher.cache(dataset)

        cached_dataset = CachedSQLiteDataset.load_dataset(
            dataset_name=self.dataset_name,
            storage_location=self.storage_location)

        self.assertEqual(len(cached_dataset), 2)

        for i in range(len(dataset)):
            tt.assert_equal(cached_dataset[i][0], dataset[i][0])
            tt.assert_equal(cached_dataset[i][1], dataset[i][1])
            self.assertEqual(cached_dataset[i][2], dataset[i][2])

if __name__ == '__main__':
    unittest.main()
