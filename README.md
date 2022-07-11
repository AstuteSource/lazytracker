# LazyTracker
Caching of functions with respect to code changes and disk-file changes

## Usage example
```python
from lazytracked import tracked

@tracked(
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