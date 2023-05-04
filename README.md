# Sorting Algorithm Testing Framework V2 PYTHON
For a University. Work in progress..

This is a sorting algorithm testing framework created as part of a university project. It currenctly includes seven well-known sorting algorithms: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort, Heap Sort and Radix Sort. 

The framework generates datasets with data of different types, sizes and distributions, and runs each sorting algorithm on the generated data multiple times to obtain an accurate measurement for its performance. Finally, it returns a dictionary containing a Pandas DataFrame for each sorting algorithm with information about the data type, data size, and execution time, and computes detailed graphs for ease of visualisation

The main purpose of this framework is to measure and compare the performance of different sorting algorithms on various types and sizes of input data. The performance is measured in terms of the execution time for each algorithm.

## Usage
To use this framework, you need to have Python and the following libraries installed: seaborn, matplotlib, pandas, and numpy. You can install these libraries using pip:

`pip install seaborn matplotlib pandas numpy`

To run an experiment, you need to call the `run_experiment function`, which takes four arguments:

* `algorithms`: a list of the sorting algorithms you want to test (e.g., [bubble_sort, selection_sort, insertion_sort]).
* `data_types`: a list of strings representing the types of data you want to generate (e.g., ['sorted', 'reverse', 'almost_sorted', 'unique', 'nonunique', 'float', 'negative']).
* `sizes`: a list of integers representing the sizes of the data you want to generate (e.g., [1000, 5000, 10000]).
* `num_runs`: an integer representing the number of times you want to run each sorting algorithm on each type and size of data.

