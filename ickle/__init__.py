import numpy as np

__version__ = '0.0.1'

class DataFrame:

    def __init__(self, data):
        """
        A DataFrame holds two dimensional heterogenous data.
        Create it by passing a dictionary of NumPy arrays to the values parameter.

        Parameters
        1. data (dict): A dictionary of strings mapped to NumPy arrays. The key will
        become the column name.
        """

        # Check for correct input types
        self._check_input_types(data)

        # Check for equal array lengths
        self._check_array_lengths(data)

    def _check_input_types(self,data):
        if not isinstance(data, dict):
            raise TypeError('`data` can accept only dictionaries')
        for key, value in data.items():
            if not isinstance(key, str):
                raise TypeError('keys of `data` must be of type str')
            if not isinstance(value, np.ndarray):
                raise TypeError('values of `data` must be NumPy arrays')
            if value.ndim != 1:
                raise ValueError('values of `data` must be some one-dimensional array')
    
    # Each column of data in the DataFrame must have the same number of elements.
    def _check_array_lengths(self,data):
        for i,value in enumerate(data.values()):
            if i == 0:
                length = len(value)
            elif length != len(value):
                raise ValueError('All arrays must be of the same length')


