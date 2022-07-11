# Lazy Tracker
Caching of functions with respect to code changes and disk-file changes

## Use Case
Data processing in data-science can be very computationally expensive. Therefore, it is useful to cache some steps of the processing pipeline. Python already has memoize functionality by default, but it only considers input and output parameter values. Unfortunately, it is not always possible and efficient to separate data loading from processing, and although the path to the file has not changed, the data may have changed.

Here LazyTracker comes to the rescue - a simple tool that allows you to cache functions that have dependencies on files stored on disk

## Usage example
```python
from lazytracked import tracked

@cached(
    input_dirs=["input_dir"],
    output_dirs=["output_dir"]
)
def expensive_function(input_dir: str, output_dir: str, parameter: int) -> int:
    ...

# This will be run for the first time. If nothing changes in input_dir, expensive_function code or parameter, 
# this will be not run again - the cashed result will be saved
result = expensive_function(
    input_dir="/input/dir",
    output_dir="/output/dir",
    parameter=5
)
```

For full example, check [Notebook Example](example/example.ipynb)