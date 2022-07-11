from dataclasses import dataclass
import shelve
import os
from textwrap import wrap
from typing import Callable, List, Optional
from lazytracker.lazytracker import LazyTracker
from dill import Pickler, Unpickler
from functools import wraps

shelve.Pickler = Pickler
shelve.Unpickler = Unpickler

def tracked(
    cache_dir: str = ".lazytracker",
    input_files: Optional[List[str]] = None,
    input_dirs: Optional[List[str]] = None,
    output_dirs: Optional[List[str]] = None,
    output_files: Optional[List[str]] = None,
):
    def inner_func(function: Callable):
        @wraps(function)
        def wrapper(**kwargs):
            os.makedirs(f"{cache_dir}", exist_ok=True)
            with shelve.open(f"{cache_dir}/tracked_functions", 'c') as db:
                input_tracker = LazyTracker()
                input_tracker.add_picklables([function])
                input_tracker.add_hparams(kwargs)
                if input_dirs is not None:
                    input_dirs_values = [kwargs[input_dir] for input_dir in input_dirs]
                    input_tracker.add_directories(input_dirs_values)
                if input_files is not None:
                    input_files_values = [kwargs[input_file] for input_file in input_files]
                    input_tracker.add_files(input_files_values)

                test_output_tracker = LazyTracker()
                if output_dirs is not None:
                    output_dirs_values = [kwargs[output_dir] for output_dir in output_dirs]
                    test_output_tracker.add_directories(output_dirs_values)
                if output_files is not None:
                    output_files_values = [kwargs[output_file] for output_file in output_files]
                    test_output_tracker.add_files(output_files_values)

                input_hash = input_tracker.hash()
                output_hash = test_output_tracker.hash()

                if input_hash in db and db[input_hash]["hash"] == output_hash:
                    return db[input_hash]["return_value"]
                else:
                    return_value = function(**kwargs)

                    output_tracker = LazyTracker()
                    if output_dirs is not None:
                        output_dirs_values = [kwargs[output_dir] for output_dir in output_dirs]
                        output_tracker.add_directories(output_dirs_values)
                    if output_files is not None:
                        output_files_values = [kwargs[output_file] for output_file in output_files]
                        output_tracker.add_files(output_files_values)

                    db[input_hash] = {
                        "return_value": return_value,
                        "hash": output_tracker.hash()
                    }

        return wrapper

    return inner_func
            

            

    return tracked_fn