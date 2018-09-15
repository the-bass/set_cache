# Set Cache

Some datasets are too big to be loaded into memory. This module provides methods to cache the dataset in a database and load each example as needed.

Last tested with **Python 3.6.4 :: Anaconda, Inc.** and **torch 0.4.1**.

## Installation

Clone this repository and run

```py
pip install .
```

inside the root directory to make the module available as `set_cache`.

## Usage example

Cache a PyTorch Dataset `AudioDataset` as `audio_dataset` in an *SQLite* database. A sample of the given dataset is expected to be of the form

```
(torch.Tensor, torch.Tensor, string)
```

, where the 2 tensors would be the x and y values and the string can be used as an identifier of the sample.

```py
from audio_dataset import AudioDataset
from set_cache import SQLiteDatasetCacher


dataset = AudioDataset()
cacher = SQLiteDatasetCacher(dataset_name='audio_dataset')

cacher.cache(dataset)
```

From now on you can load the dataset in the form of a regular PyTorch Dataset like:

```py
from set_cache import CachedSQLiteDataset


dataset = CachedSQLiteDataset.load_dataset(dataset_name=dataset_name)
```

## Development

*Unless noted otherwise, all commands are expected to be executed from the root directory of this repository.*

### Building the package for local development

To make the package available locally while making sure changes to the files are reflected immediately, run

```sh
pip install -e .
```

### Test suite

Run all tests using

```sh
python -m unittest discover tests
```
