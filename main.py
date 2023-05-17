import os

from algorithms_module.algorithms import *
from experiment_design_module.run_experiment import run_experiment
from visualisation_module.plot_results import plot_results
from visualisation_module.prot_raw_data_area import plot_raw_data_area


def main():
    algorithms = [bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort, radix_sort, bucket_sort, tim_sort]
    data_types = ['sorted', 'reverse', 'almost_sorted', 'unique', 'nonunique', 'float', 'negative']
    sizes = [500, 750, 1000, 2500, 5000, 7500, 10_000, 12_000]  # big dataset
    # sizes = [50, 75, 100, 200, 300, 400, 500, 600, 700, 750]  # small dataset
    # sizes = [500, 750, 1000]  # test
    num_runs = 6

    if not os.path.exists('plots'):
        os.makedirs('plots')
    if not os.path.exists('csvs'):
        os.makedirs('csvs')

    results = run_experiment(algorithms, data_types, sizes, num_runs)
    plot_results(results, data_types)
    plot_raw_data_area(data_types, sizes)


if __name__ == "__main__":
    main()
