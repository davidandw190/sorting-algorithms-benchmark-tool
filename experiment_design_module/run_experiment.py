import os
from typing import List

import pandas as pd

from data_generation_module.generate_data import generate_data
from performance_evaluation_module.time_and_memory import time_and_memory


def run_experiment(algorithms: List[callable], data_types: List[str], sizes: List[int], num_runs: int) -> dict:
    """Runs the experiments on the given set of algorithms, data types and sizes.

    Args:
    - algorithms: A list of callable objects representing algorithms to be tested.
    - data_types: A list of strings representing data types to be generated for testing.
    - sizes: A list of integers representing the sizes of data to be generated for testing.
    - num_runs: The number of times to run each algorithm for each combination of data type and size.

    Returns:
    - A dictionary containing the results of the experiments, where the keys are the names of the algorithms and
    the values are pandas DataFrames containing the experiment results.

    """

    data, results, results_csv = {}, {}, {}
    for data_type in data_types:
        data[data_type] = {}
        for size in sizes:
            data[data_type][size] = generate_data(size, data_type).tolist()

    for algorithm in algorithms:
        algorithm_results = []
        algorithm_results_csv = []

        for data_type in data_types:

            for size in sizes:
                arr = data[data_type][size]
                elapsed_time_sum = 0
                memory_usage_sum = 0

                for i in range(num_runs):
                    elapsed_time, memory_usage = time_and_memory(algorithm, arr)
                    elapsed_time_sum += elapsed_time
                    memory_usage_sum += memory_usage

                elapsed_time = elapsed_time_sum / num_runs
                memory_usage = memory_usage_sum / num_runs

                # Checks if elapsed time or memory usage is negligable
                if elapsed_time == 0.0:
                    elapsed_time_csv = "negligible"
                else:
                    elapsed_time_csv = elapsed_time

                if memory_usage == 0.0:
                    memory_usage_csv = "negligible"
                else:
                    memory_usage_csv = memory_usage

                algorithm_results.append((data_type, size, elapsed_time, memory_usage))
                algorithm_results_csv.append((data_type, size, elapsed_time_csv, memory_usage_csv))

        results[algorithm.__name__] = pd.DataFrame(algorithm_results,
                                                   columns=['Data Type', 'Size', 'Time', 'Memory Usage'])
        results_csv[algorithm.__name__] = pd.DataFrame(algorithm_results_csv,
                                                   columns=['Data Type', 'Size', 'Time', 'Memory Usage'])

        csv_folder_path = os.path.join(os.getcwd(), 'csvs')

        if not os.path.exists(csv_folder_path): # This is not necesarry since we already do this in main. Might change this
            os.makedirs(csv_folder_path)

        csv_file_path = os.path.join(csv_folder_path, algorithm.__name__ + '_time_memory_usage.csv')
        results_csv[algorithm.__name__].to_csv(csv_file_path, index=False)

    return results

