import numpy as np
import pandas as pd


def generate_data(n: int, data_type: str) -> pd.Series:
    """
    Generates data according to the specified type.

    Args:
    n (int): The number of data points to generate.
    data_type (str): The type of data to generate. Must be one of the following:
    - 'sorted': Returns a series of integers in ascending order from 0 to n-1.
    - 'reverse': Returns a series of integers in descending order from n-1 to 0.
    - 'unique': Returns a series of n unique integers randomly sampled from the range 0 to n-1.
    - 'nonunique': Returns a series of n integers randomly sampled from the range 0 to n//2, with replacement.
    - 'float': Returns a series of n floating-point numbers randomly sampled from the uniform distribution [0,1).
    - 'negative': Returns a series of n floating-point numbers randomly sampled from a normal distribution with mean-n/2
     and standard deviation n/6.
    - 'almost_sorted': Returns a series of integers in ascending order from 0 to n-1, with 10% of adjacent pairs of
    elements swapped.

    Returns:
    pd.Series: A pandas Series object containing the generated data.

    Raises:
    ValueError: If an invalid data_type argument is provided.
    """
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
