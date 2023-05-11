import os
from typing import List
import seaborn as sns

from matplotlib import pyplot as plt


def plot_results(results: dict, data_types: List[str]) -> None:
    """
    Plot the average running time and memory usage of sorting algorithms for different dataset sizes and types.

    Args:
    - results: A dictionary containing the sorting algorithm names as keys and data frames with sorting results
    as values.
    - data_types: A list of strings containing the names of the dataset types to plot.

    Returns:
    - None: The function plots and saves the results to a PDF file for each data type.
    """
    alg_colors = {
        'bubble_sort': '#742edf',
        'selection_sort': '#1f77b4',
        'insertion_sort': '#ff7f0e',
        'quick_sort': '#2ca02c',
        'merge_sort': '#d62728',
        'heap_sort': '#9467bd',
        'radix_sort': '#8c564b',
        'bucket_sort': '#e377c2',
        'tim_sort': '#7f7f7f'
    }
    markers, line_styles = ['o', '^', 's', 'D', 'P', 'v', 'd', 'o', '^'], ['-', '-.', '--', '-.', ':', '-', '--', '-.', ':']
    sns.set(style='whitegrid', context='paper', font_scale=1.2, palette=list(alg_colors.values()))

    for data_type in data_types:

        fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 12), dpi=300)
        sns.set_style("whitegrid", {'axes.grid': True, 'grid.linestyle': '-.', 'grid.color': 'grey'})

        axs[0].set_title(f'Average Running Time on (small) {data_type.capitalize()} Data', fontsize=18)
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

        axs[1].set_title(f'Average Memory Usage on (small) {data_type.capitalize()} Data', fontsize=18)
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
