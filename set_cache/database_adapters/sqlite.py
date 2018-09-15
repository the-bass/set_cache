import sqlite3
import torch
import numpy as np
import io


class SQLite:

    def __init__(self):
        self.__register_tensor_adapter__()
        self.__register_tensor_converter__()

    def __register_tensor_adapter__(self):
        def tensor_to_binary(tensor):
            out = io.BytesIO()
            torch.save(tensor, out)
            out.seek(0)
            return sqlite3.Binary(out.read())

        sqlite3.register_adapter(torch.Tensor, tensor_to_binary)

    def __register_tensor_converter__(self):
        def binary_to_tensor(binary):
            out = io.BytesIO(binary)
            out.seek(0)
            return torch.load(out)

        sqlite3.register_converter('TENSOR', binary_to_tensor)

    def connect(self, database_name):
        connection = sqlite3.connect(
            database_name,
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        return connection
