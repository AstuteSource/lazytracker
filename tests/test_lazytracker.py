import os
import shutil
from tempfile import TemporaryDirectory, tempdir
from lazytracker import LazyTracker

def test_hparams():
    hparams_1 = {
        'a': 1,
        'b': 2,
        'c': {
            'd': 1
        }
    }

    hparams_2 = {
        'a': 1,
        'b': 2,
        'c': {
            'd': 2
        }
    }

    tracker_1 = LazyTracker()
    tracker_1.add_hparams(hparams_1)

    tracker_2 = LazyTracker()
    tracker_2.add_hparams(hparams_1)

    tracker_3 = LazyTracker()
    tracker_3.add_hparams(hparams_2)

    assert tracker_1.hash() == tracker_2.hash()
    assert tracker_1.hash() != tracker_3.hash()

def test_picable_function():
    def func_1(x):
        return x+1
    def func_2(x):
        return x+2

    tracker_1 = LazyTracker()
    tracker_1.add_picklables([func_1])

    tracker_2 = LazyTracker()
    tracker_2.add_picklables([func_1])

    tracker_3 = LazyTracker()
    tracker_3.add_hparams([func_2])

    assert tracker_1.hash() == tracker_2.hash()
    assert tracker_1.hash() != tracker_3.hash()

def test_files():
    with TemporaryDirectory() as tmpdir:
        with open(f'{tmpdir}/a.txt', 'w') as f:
            f.write("test file 1")

        with open(f'{tmpdir}/b.txt', 'w') as f:
            f.write("test file 1")

        with open(f'{tmpdir}/c.txt', 'w') as f:
            f.write("test file 2")
                
        tracker_1 = LazyTracker()
        tracker_1.add_files([f"{tmpdir}/a.txt"])

        tracker_2 = LazyTracker()
        tracker_2.add_files([f"{tmpdir}/b.txt"])

        tracker_3 = LazyTracker()
        tracker_3.add_files([f"{tmpdir}/c.txt"])

        assert tracker_1.hash() == tracker_2.hash()
        assert tracker_1.hash() != tracker_3.hash()

def test_directories():
    with TemporaryDirectory() as tmpdir:
        os.makedirs(f"{tmpdir}/1", exist_ok=True)

        with open(f'{tmpdir}/1/a.txt', 'w') as f:
            f.write("test file 1")

        with open(f'{tmpdir}/1/b.txt', 'w') as f:
            f.write("test file 1")

        with open(f'{tmpdir}/1/c.txt', 'w') as f:
            f.write("test file 2")

        shutil.copytree(f"{tmpdir}/1", f"{tmpdir}/2")
        shutil.copytree(f"{tmpdir}/1", f"{tmpdir}/3")

        with open(f'{tmpdir}/3/c.txt', 'w') as f:
            f.write("test file 2 edited")

        tracker_1 = LazyTracker()
        tracker_1.add_directories([f"{tmpdir}/1"])

        tracker_2 = LazyTracker()
        tracker_2.add_directories([f"{tmpdir}/2"])

        tracker_3 = LazyTracker()
        tracker_3.add_directories([f"{tmpdir}/3"])

        assert tracker_1.hash() == tracker_2.hash()
        assert tracker_1.hash() != tracker_3.hash()