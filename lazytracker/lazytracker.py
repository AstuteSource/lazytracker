import hashlib
import os
from typing import Any, List
import dill
from pathlib import Path


class LazyTracker:
    def __init__(self):
        """LazyTracked enables you to compute combined hash of things like files, directories, python objects etc."""
        self._hasher = hashlib.md5()

    def add_directories(self, directories: List[str], chunk_num_blocks=128):
        """Include hash of all files inside directory (including files in subdirectories)

        Args:
            directories (List[str]): List of directories to take files from
            chunk_num_blocks (int, optional): How many chunks to read at once. Defaults to 128.
        """
        files_to_check = []

        for directory in directories:
            files_to_check.extend(list(Path(directory).rglob("*")))

        files_to_check = sorted(files_to_check)

        self.add_files(files_to_check, chunk_num_blocks)

    def add_files(self, filepaths: List[str], chunk_num_blocks=128):
        """Include hash of files

        Args:
            filepaths (List[str]): List of paths to files
            chunk_num_blocks (int, optional): How many chunks to read at once. Defaults to 128.
        """
        for p in filepaths:
            if os.path.exists(p):
                with open(p, "rb") as f:
                    while chunk := f.read(chunk_num_blocks * self._hasher.block_size):
                        self._hasher.update(chunk)
            else:
                self._hasher.update(dill.dumps(None))

    def add_hparams(self, hparams: dict):
        """Add hash of python dictionary. Utility function for storing pickable

        Args:
            hparams (dict): A dictionary to be included
        """
        self.add_picklables([hparams])

    def add_picklables(self, objects: List[Any], recursive: bool=False):
        """Include hash of any picklable python objects (pickable by dill)

        Args:
            objects (List[Any]): List of python objects to hash
            recursive (bool): Wheter to track dependencies of object. Eg.: if function calls another function, if 
                recursive is set to true the changes in inner function are also tracked
        """
        for obj in objects:
            self._hasher.update(dill.dumps(obj, recurse=recursive))

    def hash(self) -> str:
        """Compute hash

        Returns:
            str: Computed checksum of all things tracked
        """

        return self._hasher.hexdigest()
