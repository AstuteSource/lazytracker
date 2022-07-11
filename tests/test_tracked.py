from tempfile import TemporaryDirectory
from lazytracker import cached


def test_cached():
    with TemporaryDirectory() as cache_dir:
        updated = False

        @cached(
            cache_dir=cache_dir,
            input_dirs=["input_dir"],
            output_dirs=["output_dir"]
        )
        def test_function(input_dir: str, output_dir: str, parameter: int):
            nonlocal updated

            with open(f"{output_dir}/test.txt", 'w') as f:
                f.write(str(parameter))

            updated = True
            return parameter

        with TemporaryDirectory() as input_dir:
            with open(f"{input_dir}/test.txt", 'w') as f:
                f.write("test_file")

            with TemporaryDirectory() as output_dir:
                assert test_function(
                    input_dir=input_dir, 
                    output_dir=output_dir, 
                    parameter=3
                ) == 3
                assert updated == True

                # Don't change antything
                updated = False
                assert test_function(
                    input_dir=input_dir, 
                    output_dir=output_dir, 
                    parameter=3
                ) == 3
                assert updated == False

                # Change parameter
                assert test_function(
                    input_dir=input_dir, 
                    output_dir=output_dir, 
                    parameter=5
                ) == 5
                assert updated == True

                # Change input dependency
                updated = False
                with open(f"{input_dir}/test.txt", 'w') as f:
                    f.write("changed_test_file")

                assert test_function(
                    input_dir=input_dir, 
                    output_dir=output_dir, 
                    parameter=5
                ) == 5
                assert updated == True

                # Corrupt output
                with open(f"{output_dir}/test.txt", 'w') as f:
                    f.write("corrupted output")

                assert test_function(
                    input_dir=input_dir, 
                    output_dir=output_dir, 
                    parameter=5
                ) == 5
                assert updated == True
