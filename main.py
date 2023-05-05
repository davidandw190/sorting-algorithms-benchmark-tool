import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import time
import tracemalloc
import itertools

from algorithms import *


def generate_data(n: int, data_type: str) -> pd.Series:
    if data_type == 'sorted':
        return pd.Series(np.arange(n))
    elif data_type == 'reverse':
        return pd.Series(np.arange(n)[::-1])
    elif data_type == 'unique':
        return pd.Series(np.random.permutation(n))
    elif data_type == 'nonunique':
        data = np.random.randint(0, n//2, size=n//2)
        data = np.concatenate((data, data))
        return pd.Series(np.random.permutation(data))
    elif data_type == 'float':
        return pd.Series(np.random.normal(0, 1, size=n))
    elif data_type == 'negative':
        return pd.Series(np.random.normal(0, n/2, size=n))
    else:
        raise ValueError('Invalid data type')

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
    plot_raw_data_area(data_types, sizes)  # plot raw data area

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


# def plot_data(data):
#     fig, ax = plt.subplots(len(data), len(data[0]), figsize=(15,15))
#     for i, row in enumerate(data):
#         for j, dataset in enumerate(row):
#             x = np.arange(len(dataset))
#             y = dataset
#             ax[i,j].fill_between(x, y, color='cornflowerblue')
#             ax[i,j].plot(x, y, color='navy', linewidth=1.5)
#             ax[i,j].set_title(f"{len(dataset)} elements: {data_types[i]}", fontsize=12)
#             ax[i,j].set_xlabel('Index', fontsize=10)
#             ax[i,j].set_ylabel('Value', fontsize=10)
#             ax[i,j].tick_params(axis='both', which='major', labelsize=8)
#     fig.tight_layout()
#     plt.show()

def plot_raw_data_area(data_types, sizes):
    cmap = plt.get_cmap('viridis', len(data_types))
    chunks = list(itertools.zip_longest(*[iter(data_types)] * 3, fillvalue=None))

    for j, group in enumerate(chunks):
        fig, ax = plt.subplots(3, 1, figsize=(10, 10), sharey=True, dpi=300)

        for i, data_type in enumerate(group):
            if data_type is not None:
                arr = generate_data(1000, data_type)
                x = np.arange(1000)
                ax[i].fill_between(x, arr, color=cmap(data_types.index(data_type)), alpha=0.7, label=data_type)
                ax[i].plot(x, arr, color='black', linewidth=1.5)
                ax[i].set_title(rf'{data_type.capitalize()} data', fontsize=16, color='navy')
                ax[i].set_xlabel('Index', fontsize=12, color='black')
                ax[i].set_ylabel('Value', fontsize=12, color='black')
                ax[i].set_ylim([min(arr) - 0.1*(max(arr)-min(arr)), max(arr) + 0.1*(max(arr)-min(arr))])
                ax[i].set_yticks([min(arr), max(arr)])
                ax[i].legend(loc='upper right', fontsize=8)

        fig.suptitle(rf'Raw data area plot - Group {j+1}', fontsize=18, color='navy')
        plt.tight_layout()

        if not os.path.exists('raw_data'):
            os.makedirs('raw_data')

        plt.savefig(f'raw_data/raw_data_area_plot_1000_group{j+1}.pdf', dpi=300, bbox_inches='tight', pad_inches=0.2)

def plot_results(results):
    # Define colors for each algorithm
    alg_colors = {
        'selection_sort': 'tab:blue',
        'insertion_sort': 'tab:orange',
        'quick_sort': 'tab:green'
    }

    # Define data types to plot
    data_types = ['sorted', 'reverse', 'unique', 'float', 'negative']

    # Loop over data types
    for data_type in data_types:
        # Create figure with two subplots
        fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(8, 10), dpi=300)

        # Plot running time on first subplot
        axs[0].set_title(f'Average Running Time on {data_type.capitalize()} Data', fontsize=18)
        axs[0].set_xlabel('Dataset Size', fontsize=14)
        axs[0].set_ylabel('Average Running Time (seconds)', fontsize=14)
        axs[0].tick_params(axis='both', which='major', labelsize=12)
        axs[0].grid(True)
        for algorithm, df in results.items():
            agg_df = df[df['Data Type'] == data_type].groupby('Size')['Time'].agg(['mean', 'std']).reset_index()
            axs[0].plot(agg_df['Size'], agg_df['mean'], label=algorithm.capitalize(), marker='o',
                        color=alg_colors[algorithm])
            axs[0].fill_between(agg_df['Size'], agg_df['mean'] - agg_df['std'], agg_df['mean'] + agg_df['std'],
                                alpha=0.2, color=alg_colors[algorithm])
        axs[0].legend(loc='best', fontsize=12)

        # Plot memory usage on second subplot
        axs[1].set_title(f'Average Memory Usage on {data_type.capitalize()} Data', fontsize=18)
        axs[1].set_xlabel('Dataset Size', fontsize=14)
        axs[1].set_ylabel('Average Memory Usage (KB)', fontsize=14)
        axs[1].tick_params(axis='both', which='major', labelsize=12)
        axs[1].grid(True)
        for algorithm, df in results.items():
            agg_df = df[df['Data Type'] == data_type].groupby('Size')['Memory Usage'].agg(['mean', 'std']).reset_index()
            axs[1].plot(agg_df['Size'], agg_df['mean'], label=algorithm.capitalize(), marker='o',
                        color=alg_colors[algorithm])
            axs[1].fill_between(agg_df['Size'], agg_df['mean'] - agg_df['std'], agg_df['mean'] + agg_df['std'],
                                alpha=0.2, color=alg_colors[algorithm])
        axs[1].legend(loc='best', fontsize=12)

        # Save figure to file
        fig.tight_layout()
        fig.savefig(os.path.join('plots', f'{data_type}_plot.png'), dpi=300)
        plt.show()
        plt.close(fig)

def main():
    sns.set_style('whitegrid')
    sns.set_palette(['#1f77b4', '#ff7f0e', '#2ca02c'])

    # plt.rcParams.update({
    #     'font.family': 'serif',
    #     'font.serif': ['Times New Roman'],
    #     'font.size': 14,
    #     'axes.labelsize': 16,
    #     'axes.titlesize': 18,
    #     'xtick.labelsize': 14,
    #     'ytick.labelsize': 14,
    #     'legend.fontsize': 14,
    #     'figure.figsize': (8, 6),
    #     'figure.dpi': 300,
    # })

    algorithms = [selection_sort, insertion_sort, quick_sort]
    data_types = ['sorted', 'reverse']
    sizes = [10, 100, 1000, 2000, 5000]
    num_runs = 1

    if not os.path.exists('plots'):
        os.makedirs('plots')
    if not os.path.exists('csvs'):
        os.makedirs('csvs')

    results = run_experiment(algorithms, data_types, sizes, num_runs)
    plot_results(results)


if __name__ == "__main__":
    main()
