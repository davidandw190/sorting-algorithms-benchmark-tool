# Sorting Algorithm Benchmarking Framework V2 PYTHON

The Sorting Algorithms Benchmarking Framework is a flexible and scalable benchmarking tool built in Python to study and compare the performance of various sorting algorithms under different test cases. This project is designed to be scalable, modular, and easy to use, and is aimed at conducting accurate and exhaustive evaluations of sorting algorithms' properties, their performance, and their suitability for use cases, examining their performances under conditions such as data sizes, data types, and data distributions.

This project was developed as a part of a research project during my Methods and Practices in Computer Science course in the first year of my Bachelor's Degree. The requirement of the project was to study sorting algorithms' behavior and performance.

## Table of Contents

  1. [FEATURES](https://github.com/davidandw190/Sorting-Algorithm-Exp-Framework-V2-PYTHON#features)
  2. [SETUP](https://github.com/davidandw190/Sorting-Algorithm-Exp-Framework-V2-PYTHON#setup)
  3. [CONFIGURATION](https://github.com/davidandw190/Sorting-Algorithm-Exp-Framework-V2-PYTHON#configuration)
  4. [USAGE](https://github.com/davidandw190/Sorting-Algorithm-Exp-Framework-V2-PYTHON#usage)
  5. [CONTRIBUTION](https://github.com/davidandw190/Sorting-Algorithm-Exp-Framework-V2-PYTHON#contribution)
  

## Features

The Sorting Algorithms Testing Framework includes the following features:

* **Modular Design:** The framework is composed of five modules, including `Data_Generation_Module`, `Algorithms_Module`, `Performance_Evaluation_Module`, `Experiment_Design_Module`, and `Visualization_Module`, allowing users to customize and extend the framework as needed.

* **Multiple Sorting Algorithms:** The framework currently includes nine sorting algorithms, including:
 `Bubble Sort`, `Insertion Sort`, `Merge Sort`, `Quick Sort`, `Heap Sort`, `Radix Sort`, `Counting Sort`, `Bucket Sort`, and `Tim Sort`.

* **Various Test Cases:** The framework supports testing on various test cases, including `TIME PERFORMANCE` and `MEMORY USAGE`.

* **Different Data Sizes:** The framework can test sorting algorithms on various data sizes.

* **Different Data Types:** The framework supports different data types, such as `INTEGERS`, `FLOATS`, and `NEGATIVES`.

* **Different Data Distributions:** The framework allows users to test sorting algorithms on different data distributions, such as: `SORTED`, `REVERSE`, `ALMOST SORTED`, `UNIQUE`, and `NON-UNIQUE`.
 
* **Visualizations:** The framework includes various visualization methods, such as computing detailed PDF plots and graphs, as well as CSV files, to help users analyze and compare the results.


## SETUP

To use the experimental framework, please follow these installation instructions:

1. Make sure you have Python 3.x installed on your system. If not, you can download it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/).

2. Clone or download the project from the GitHub repository: [https://github.com/davidandw190/Sorting-Algorithm-Exp-Framework-V2-PYTHON.git](https://github.com/davidandw190/Sorting-Algorithm-Exp-Framework-V2-PYTHON.git).

3. Navigate to the project directory using the command line or terminal.

4. Install the required dependencies by running the following command:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the experiments, you can configure certain parameters according to your specific needs. To do this, open the `main.py` file in a text editor and locate the `main` function.

1. Algorithms: The `algorithms` list contains the algorithms that will be tested. You can modify this list to include or exclude specific algorithms. For example, if you want to test only the bubble sort and selection sort algorithms, modify the `algorithms` list as follows:

```python
algorithms = [bubble_sort, selection_sort]
```
2. Data Types: The `data_types` list specifies the types of data scenarios to test the algorithms with and can be modified to include or exclude specific data types. For example, if you want to test only the `sorted` and `reverse` data types, modify the `data_types` list as follows:

```python
data_types = ['sorted', 'reverse']
```
3. Sizes: The sizes list determines the sizes of the datasets to be used in the experiments, and can, too, be modified. For example, if you want to test the algorithms with dataset sizes of 500, 750, and 1000, modify the sizes list as follows:
```python
sizes = [500, 750, 1000]
```
4. Number of Runs: The `num_runs` variable specifies the number of times each experiment will be repeated. To modify it to perform each experiment 10 times, for example, modify the `num_runs` variable as follows:
```python
num_runs = 10
```

5. Output Directories: The program creates two directories, namely `plots` and `csvs`, to store the generated plots and CSV files, respectively. If these directories do not exist, they will be created automatically. You can change the directory names or customize the directory paths by modifying the following lines:
```python
if not os.path.exists('plots'):
    os.makedirs('plots')
if not os.path.exists('csvs'):
    os.makedirs('csvs')
```    
## Usage
To run the experiments and visualize the results, follow these steps:

* Open a command line or terminal.

* Navigate to the project directory.

* Run the following command:
```python
python main.py
```
The program will execute the experiments using the configured parameters and generate the necessary output files:
  * for each datatype given, a plot showcasing the `time perfromance` and `memory usage` of the algorithms on that datatype, by default found in `/plots`
  * for each algorithms given, a CSV file showcasing the average `time perfromance` and `memory usage` of the algorithm on each datatype  and size, by default found in `/csvs`
  * a group of area plots, number of which is determined by the number of dataypes used showcasing a sample of `raw data` used for the experiment, by default found in `/raw_data`
 
## Contribution

