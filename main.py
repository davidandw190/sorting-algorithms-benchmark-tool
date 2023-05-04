import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import time
import tracemalloc

from algorithms import *


def generate_data(n, data_type):
    if data_type == 'sorted':
        return np.arange(n)
    elif data_type == 'reverse':
        return np.arange(n)[::-1]
    elif data_type == 'almost_sorted':
        arr = np.arange(n)
        np.random.shuffle(arr)
        return arr
    elif data_type == 'unique':
        return np.random.choice(2 * n, n, replace=False)
def time_function(func, arr):
    start_time = time.monotonic()
    func(arr)
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    return elapsed_time

def measure_memory_usage(func, arr):
    tracemalloc.start()
    func(arr)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_usage = peak / 1024
    return memory_usage
def run_experiment(algorithms, data_types, sizes, num_runs):
    data, results, results_csv = {}, {}, {}

    for data_type in data_types:
        data[data_type] = {}
        for size in sizes:
            data[data_type][size] = generate_data(size, data_type)

    for algorithm in algorithms:
        algorithm_results = []
        algorithm_results_csv = []

        for data_type in data_types:

            for size in sizes:
                arr = data[data_type][size]
                elapsed_time_sum = 0
                memory_usage_sum = 0

                for i in range(num_runs):
                    elapsed_time_sum += time_function(algorithm, arr)
                    memory_usage_sum += measure_memory_usage(algorithm, arr)

                elapsed_time = elapsed_time_sum / num_runs
                memory_usage = memory_usage_sum / num_runs

                # Check if elapsed time or memory usage is negligable
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


def plot_results(results):
    sns.set_style('darkgrid')
    alg_colors = {'selection_sort': 'tab:blue',
                  'insertion_sort': 'tab:orange',
                  'quick_sort': 'tab:green'}
    for data_type in ['sorted', 'reverse']:
        plt.figure(figsize=(8, 6), dpi=300)
        for algorithm, df in results.items():
            agg_df = df[df['Data Type'] == data_type].groupby('Size')['Time'].agg(['mean', 'std']).reset_index()
            plt.plot(agg_df['Size'], agg_df['mean'], label=algorithm.capitalize(), marker='o', color=alg_colors[algorithm])
            plt.fill_between(agg_df['Size'], agg_df['mean'] - agg_df['std'], agg_df['mean'] + agg_df['std'], alpha=0.2, color=alg_colors[algorithm])
        plt.title(f'Performance on {data_type.capitalize()} Data', fontsize=18)
        plt.xlabel('Dataset Size', fontsize=14)
        plt.ylabel('Average Running Time (seconds)', fontsize=16)
        plt.tick_params(axis='both', which='major', labelsize=14)
        plt.legend(loc='best', fontsize=14)
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(os.path.join('plots', f'{data_type}_plot.png'), dpi=300)
        plt.show()


def main():
    algorithms = [selection_sort, insertion_sort, quick_sort]
    data_types = ['sorted', 'reverse']
    sizes = [10, 100, 500, 1000]
    num_runs = 2

    if not os.path.exists('plots'):
        os.makedirs('plots')
    if not os.path.exists('csvs'):
        os.makedirs('csvs')

    results = run_experiment(algorithms, data_types, sizes, num_runs)
    plot_results(results)


if __name__ == "__main__":
    main()
