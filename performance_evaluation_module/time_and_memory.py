import tracemalloc
import time


def time_and_memory(func: callable, arr: list) -> tuple:
    """
    Measures the time and memory usage of an algorithm applied to an array.

    Args:
    - func: a callable that takes an array as input and performs some operation.
    - arr: a list or numpy array to be used as input to the function.

    Returns:
    - A tuple containing the elapsed time (in seconds) and peak memory usage (in kilobytes).
    """

    start_time = time.monotonic()
    tracemalloc.start()
    func(arr)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    memory_usage = peak / 1024
    return elapsed_time, memory_usage

