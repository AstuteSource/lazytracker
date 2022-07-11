import hashlib
from typing import Any, List
import dill
from pathlib import Path

class LazyTracker:
    def __init__(self):
        self._hasher = hashlib.md5()

    def add_directories(self, directories: List[str], chunk_num_blocks=128):
        files_to_check = []

        for directory in directories:
            files_to_check.extend(list(Path(directory).rglob("*")))

        files_to_check = sorted(files_to_check)

        self.add_files(files_to_check, chunk_num_blocks)

    def add_files(self, filepaths: List[str], chunk_num_blocks=128):
        for p in filepaths:
            with open(p,'rb') as f: 
                while chunk := f.read(chunk_num_blocks*self._hasher.block_size): 
                    self._hasher.update(chunk)            

    def add_hparams(self, hparams: dict):
        self._hasher.update(
            dill.dumps(hparams)
        )

    def add_picklables(self, functions: List[Any]):
        for function in functions:
            self._hasher.update(
                dill.dumps(function)
            )

    def hash(self) -> str:
        return self._hasher.hexdigest()
    