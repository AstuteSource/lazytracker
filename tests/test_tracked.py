from tempfile import TemporaryDirectory
from lazytracker import tracked


def test_tracked():
    with TemporaryDirectory() as cache_dir:
        updated = False

        @tracked(
            cache_dir=cache_dir,
            input_dirs=["input_dir"],
            output_dirs=["output_dir"]
        )
        def test_function(input_dir: str, output_dir: str, parameter: int):
            nonlocal updated

            with open(f"{output_dir}/test.txt", 'w') as f:
                f.write(str(parameter))

            updated = True

        with TemporaryDirectory() as input_dir:
            with open(f"{input_dir}/test.txt", 'w') as f:
                f.write("test_file")

            with TemporaryDirectory() as output_dir:
                test_function(
                    input_dir=input_dir, 
                    output_dir=output_dir, 
                    parameter=3
                )
                assert updated == True

                updated = False
                test_function(
                    input_dir=input_dir, 
                    output_dir=output_dir, 
                    parameter=3
                )
                assert updated == False

                test_function(
                    input_dir=input_dir, 
                    output_dir=output_dir, 
                    parameter=5
                )
                assert updated == True

                updated = False
                with open(f"{input_dir}/test.txt", 'w') as f:
                    f.write("changed_test_file")

                test_function(
                    input_dir=input_dir, 
                    output_dir=output_dir, 
                    parameter=5
                )
                assert updated == True
