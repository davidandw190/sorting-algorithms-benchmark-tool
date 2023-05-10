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
        return pd.Series(np.arange(n, 0, -1))
    elif data_type == 'unique':
        return pd.Series(np.random.choice(np.arange(n), size=n, replace=False))
    elif data_type == 'nonunique':
        data = np.random.randint(0, n//2, size=n)
        return pd.Series(np.random.choice(data, size=n))
    elif data_type == 'float':
        return pd.Series(np.random.uniform(size=n))
    elif data_type == 'negative':
        return pd.Series(np.random.normal(loc=-n/2, scale=n/6, size=n))
    elif data_type == 'almost_sorted':
        data = np.arange(n)
        swap_idx = np.random.choice(n - 1, size=n // 10, replace=False)
        data[swap_idx] = data[swap_idx + 1]
        return pd.Series(data)
    else:
        raise ValueError('Invalid data type')


def time_and_memory(func, arr):
    start_time = time.monotonic()
    tracemalloc.start()
    func(arr)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    memory_usage = peak / 1024
    return elapsed_time, memory_usage


def run_experiment(algorithms, data_types, sizes, num_runs):
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


def plot_raw_data_area(data_types, sizes):
    cmap = plt.get_cmap('tab10', len(data_types))
    chunks = list(itertools.zip_longest(*[iter(data_types)] * 3, fillvalue=None))
    alpha = 0.5
    num_groups = len(chunks)

    for j, group in enumerate(chunks):
        num_plots = len([dt for dt in group if dt is not None])
        fig, ax = plt.subplots(num_plots, 1, figsize=(10, 5 * num_plots), sharex=True, dpi=300)

        if num_plots == 1:  # Manually creates the 1D array if num_plots is 1
            ax = [ax]

        for i, data_type in enumerate(group):
            if data_type is not None:
                arr = generate_data(sizes[j], data_type)
                x = np.arange(sizes[j])
                ax[i].fill_between(x, arr, color=cmap(data_types.index(data_type)), alpha=alpha, label=data_type)
                ax[i].plot(x, arr, color='gray', linewidth=1)
                ax[i].set_title(f'{data_type.capitalize()} Data', fontsize=16, color='black')
                ax[i].set_xlabel('Index', fontsize=14, color='black')
                ax[i].set_ylabel('Value', fontsize=14, color='black')
                ax[i].set_ylim([min(arr) - 0.1 * (max(arr) - min(arr)), max(arr) + 0.1 * (max(arr) - min(arr))])
                ax[i].set_yticks([min(arr), 0, max(arr)])
                ax[i].grid(True)
                ax[i].legend(loc='upper right', fontsize=12, frameon=False)

        fig.suptitle(f'Raw Data Area Plot - Group {j + 1}', fontsize=20, color='black')
        plt.tight_layout(pad=2)

        # Adds a zero value bar
        ax[-1].axhline(y=0, linestyle='-', color='black', linewidth=1)

        if not os.path.exists('raw_data'):
            os.makedirs('raw_data')

        plt.savefig(f'raw_data/raw_data_area_plot_group{j + 1}.pdf', dpi=300, bbox_inches='tight', pad_inches=0.2)
        plt.clf()


def plot_results(results, data_types):
    alg_colors = {
        'selection_sort': '#1f77b4',
        'insertion_sort': '#ff7f0e',
        'quick_sort': '#2ca02c',
        'merge_sort': '#d62728',
        'heap_sort': '#9467bd',
        'radix_sort': '#8c564b',
        'bucket_sort': '#e377c2',
        'tim_sort': '#7f7f7f'
    }
    markers, line_styles = ['o', 's', 'D', 'P', 'v', 'd', 'o', '^'], ['-', '--', '-.', ':', '-', '--', '-.', ':']
    sns.set(style='whitegrid', context='paper', font_scale=1.2, palette=list(alg_colors.values()))

    for data_type in data_types:

        fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 12), dpi=300)
        sns.set_style("whitegrid", {'axes.grid': True, 'grid.linestyle': '-.', 'grid.color': 'grey'})

        axs[0].set_title(f'Average Running Time on {data_type.capitalize()} Data', fontsize=18)
        axs[0].set_xlabel('Dataset Size', fontsize=14)
        axs[0].set_ylabel('Average Running Time (s)', fontsize=14)
        axs[0].tick_params(axis='both', which='major', labelsize=12)

        for algorithm, df in results.items():
            agg_df = df[df['Data Type'] == data_type].groupby('Size')['Time'].agg(['mean', 'std']).reset_index()

            # sns.lineplot(x=agg_df['Size'], y=agg_df['mean'], label=algorithm.capitalize(),
            #              marker=markers[list(alg_colors.keys()).index(algorithm)],
            #              color=alg_colors[algorithm], linewidth=2, markersize=7, ax=axs[0])

            sns.lineplot(x=agg_df['Size'], y=agg_df['mean'], label=algorithm.capitalize(),
                         marker=markers[list(alg_colors.keys()).index(algorithm)], color=alg_colors[algorithm],
                         linewidth=1.7, markersize=7, ax=axs[0],
                         linestyle=line_styles[list(alg_colors.keys()).index(algorithm)])

            axs[0].fill_between(agg_df['Size'], agg_df['mean'] - agg_df['std'], agg_df['mean'] + agg_df['std'],
                                alpha=0.2, color=alg_colors[algorithm])

        axs[0].legend(loc='upper left', fontsize=10, frameon=True, fancybox=True, facecolor='white', edgecolor='black')

        axs[1].set_title(f'Average Memory Usage on {data_type.capitalize()} Data', fontsize=18)
        axs[1].set_xlabel('Dataset Size', fontsize=14)
        axs[1].set_ylabel('Average Memory Usage (KB)', fontsize=14)
        axs[1].tick_params(axis='both', which='major', labelsize=12)

        for algorithm, df in results.items():
            agg_df = df[df['Data Type'] == data_type].groupby('Size')['Memory Usage'].agg(['mean', 'std']).reset_index()

            sns.scatterplot(x=agg_df['Size'], y=agg_df['mean'], label=algorithm.capitalize(),
                            marker=markers[list(alg_colors.keys()).index(algorithm)],
                            color=alg_colors[algorithm], linewidth=1, edgecolor='black', s=60, ax=axs[1])

            axs[1].fill_between(agg_df['Size'], agg_df['mean'] - agg_df['std'], agg_df['mean'], alpha=0.2, color=alg_colors[algorithm])
        axs[1].legend(loc='upper left', fontsize=10, frameon=True, fancybox=True, facecolor='white', edgecolor='black')

        for ax in axs:

            ax.spines['bottom'].set_color('black')
            ax.spines['left'].set_color('black')
            ax.spines['top'].set_color('black')
            ax.spines['right'].set_color('black')

            ax.spines['bottom'].set_linewidth(1.5)
            ax.spines['left'].set_linewidth(1.5)
            ax.spines['top'].set_linewidth(1.5)
            ax.spines['right'].set_linewidth(1.5)

            ax.tick_params(axis='both', which='major', labelcolor='black', labelsize=12)

        fig.subplots_adjust(hspace=0.3)
        fig.savefig(os.path.join('plots', f'{data_type}_plot.pdf'), dpi=300, bbox_inches='tight')
        plt.show()


def main():
    algorithms = [selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort, radix_sort, bucket_sort, tim_sort]
    data_types = ['sorted', 'reverse', 'almost_sorted', 'unique', 'nonunique', 'float', 'negative']
    sizes = [500, 750, 1000, 2500, 5000, 7500, 10_000, 12_000]
    # sizes = [50, 100, 250, 500, 750, 1000, 1250, 1500]
    # sizes = [500, 750, 1000]
    num_runs = 8

    if not os.path.exists('plots'):
        os.makedirs('plots')
    if not os.path.exists('csvs'):
        os.makedirs('csvs')

    results = run_experiment(algorithms, data_types, sizes, num_runs)
    plot_results(results, data_types)
    plot_raw_data_area(data_types, sizes)


if __name__ == "__main__":
    main()
