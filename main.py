
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

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
    start_time = time.time()
    func(arr)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


def run_experiment(algorithms, data_types, sizes, num_runs):
    data = {}
    for data_type in data_types:
        data[data_type] = {}
        for size in sizes:
            data[data_type][size] = generate_data(size, data_type)

    results = {}
    for algorithm in algorithms:
        algorithm_results = []
        for data_type in data_types:
            for size in sizes:
                arr = data[data_type][size]
                elapsed_time_sum = 0
                for i in range(num_runs):
                    elapsed_time_sum += time_function(algorithm, arr)
                elapsed_time = elapsed_time_sum / num_runs
                algorithm_results.append((data_type, size, elapsed_time))
        results[algorithm.__name__] = pd.DataFrame(algorithm_results, columns=['Data Type', 'Size', 'Time'])
    return results


def plot_results(results):
    for data_type in ['sorted', 'reverse', 'almost_sorted', 'unique']:
        sns.set_style('darkgrid')
        plt.figure(figsize=(10, 6), dpi=300)
        for algorithm, df in results.items():
            agg_df = df[df['Data Type'] == data_type].groupby('Size')['Time'].agg(['mean', 'std']).reset_index()
            plt.plot(agg_df['Size'], agg_df['mean'], label=algorithm.capitalize(), marker='o')
            plt.fill_between(agg_df['Size'], agg_df['mean'] - agg_df['std'], agg_df['mean'] + agg_df['std'], alpha=0.2)
        plt.title(f'Performance on {data_type.capitalize()} Data', fontsize=18)
        plt.xlabel('Dataset Size', fontsize=12)
        plt.ylabel('Avg Running Time (s)', fontsize=12)
        plt.tick_params(axis='both', which='major', labelsize=14)
        plt.legend(loc='best', fontsize=12)
        plt.grid(True)
        plt.show()


def main():
    algorithms = [selection_sort, insertion_sort, quick_sort]
    data_types = ['sorted', 'reverse', 'almost_sorted', 'unique']
    sizes = [10, 100, 500, 1000, 2500]
    num_runs = 5

    results = run_experiment(algorithms, data_types, sizes, num_runs)
    plot_results(results)


if __name__ == "__main__":
    main()


