import itertools
import os
from typing import List

import numpy as np
from matplotlib import pyplot as plt

from data_generation_module.generate_data import generate_data


def plot_raw_data_area(data_types: List[str], sizes: List[int]) -> None:
    """
    Generates area plots of raw data for different data types and sizes.

    Args:
    - data_types: A list of strings specifying the data types to generate.
    - sizes: A list of integers specifying the sizes of the data to generate.

    Returns:
    - None
    """
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

