from typing import Type
import numpy as np

__version__ = '0.0.1'

class DataFrame:

    def __init__(self, data):
        """
        A DataFrame holds two dimensional heterogenous data.
        Create it by passing a dictionary of NumPy arrays to the values parameter.

        Parameters
        -------
        1. data (dict): A dictionary of strings mapped to NumPy arrays. The key will
        become the column name.
        """

        # Check for correct input types
        self._check_input_types(data)

        # Check for equal array lengths
        self._check_array_lengths(data)

        # Convert unicode arrays to objects
        self._data = self._convert_unicode_to_object(data)

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

    def _convert_unicode_to_object(self,data):
        # All data from `data` is stored in this `new_data` dictionary
        new_data = {}
        for key, value in data.items():
            if value.dtype.kind == 'U':
                new_data[key] = value.astype('object')
            else:
                new_data[key] = value
        return new_data

    def __len__(self):
        """
        Make the built-in `len` function work with our dataframe
        Returns
        -------
        int: The number of rows in the dataframe
        """
        # Alternative Way:
        # for value in self._data.values():
            # value is a NumPy array and they already work with the `len` function
            # return len(value)
        return len(next(iter(self._data.values())))

    @property
    def columns(self):
        """
        _data holds column names mapped to arrays
        Dictionaries are ordered from Python 3.6+
        Hence using that to put columns in correct order in list

        Returns
        -------
        list of column names
        """
        # if you iterate through a dict, you only get the keys and not the values.
        return list(self._data)

    @columns.setter
    def columns(self, columns):
        """
        Must supply a list of columns as strings the same length as the current DataFrame

        Parameters
        -------
        columns: list of strings

        Returns
        -------
        None
        """
        if not isinstance(columns, list):
            raise TypeError('`columns` must be a list')
        if len(columns) != len(self._data):
            raise ValueError('Newly created `columns` must have the same length as the current DataFrame')
        for col in columns:
            if not isinstance(col, str):
                raise TypeError('All column names must be of type str')
        if len(columns) != len(set(columns)):
            raise ValueError('`columns` cannot have duplicates')
        # updating _data
        new_data = dict(zip(columns, self._data.values()))
        self._data = new_data

    @property
    def shape(self):
        """
        Returns
        -------
        Two-item tuple of no. of rows and columns
        """
        return len(self), len(self._data)

    # ToDo: Complete this method
    def _repr_html_(self):
        """
        Used to create a string of HTML to nicely display the DataFrame in a Jupyter Notebook.
        Different string formatting is used for different data types.

        The structure of HTML is as follows:
        <table>
            <thead>
                <tr>
                    <th>data</th>
                    ...
                    <th>data</th>
                </tr>
            <//thead>
            <tbody>
                <tr>
                    <td><strong>{i}</strong></td>
                    <td>data</td>
                    ...
                    <td>data</td>
                </tr>
                ...
                <tr>
                    <td><strong>{i}</strong></td>
                    <td>data</td>
                    ...
                    <td>data</td>
                </tr>
            </tbody>
        </table>
        """
        pass

    @property
    def values(self):
        """
        Returns
        -------
        A single 2D NumPy array of all the columns of data. 
        """
        # https://numpy.org/doc/stable/reference/generated/numpy.column_stack.html
        return np.column_stack(list(self._data.values()))

    @property
    def dtypes(self):
        """
        Returns
        -------
        A two-column DataFrame of column names in one column and their data type in the other
        """
        DTYPE_NAME = {'O': 'string', 'i': 'int', 'f': 'float', 'b': 'bool'}
        col_names = np.array(self.columns)
        dtypes = []
        for value in self._data.values():
            kind = value.dtype.kind
            dtype = DTYPE_NAME[kind]
            dtypes.append(dtype)
        new_data = {'Column Name': col_names, 'Data Type': np.array(dtypes)}

        return DataFrame(new_data)

    def __getitem__(self, item):
        """
        Use the brackets operator to simutaneously select rows and columns

        A single string selects one column -> df['colname']
        A list of strings selects multiple columns -> df[['colname1','colname2']]
        A one column DataFrame of boolean that filters rows -> df[df_bool]

        Row and column selection simultaneously -> df[rs, cs]
            where cs and rs can be integers, slices, or a list of integers
            rs can also be a one-column boolean DataFrame

        Returns
        -------
        A subset of the original DataFrame
        """
        # select a single column -> df['colname']
        if isinstance(item, str):
            return DataFrame({item: self._data[item]})
        
        # select multiple columns -> df[['colname1', 'colname2' ]]
        if isinstance(item, list):
            return DataFrame({col: self._data[col] for col in item})
        
        # boolean selection -> df['height'] > 5.5
        if isinstance(item, DataFrame):
            if item.shape[1] != 1:
                raise ValueError('Only pass a single- column DataFrame for selection')
            # _data.values()[0] cannot be used as
            # 'dict_values' doesn't allow indexing
            arr = next(iter(item._data.values()))
            if arr.dtype.kind != 'b':
                raise ValueError('item must be a one-column boolean DataFrame')
            # value[arr] -> NumPy does boolean selection. 
            return DataFrame({col: value[arr] for col, value in self._data.items()})
        
        if isinstance(item, tuple):
            return self._getitem_tuple(item)
        else:
            raise TypeError('Selection can be made only with a string, a list or a tuple')

    def _getitem_tuple(self, item):
        # simultaneous selection of rows and columns -> df[row, col]
        if len(item) != 2:
            raise ValueError('Pass either a single string or a two-item tuple inside the selection operator.')
        row_selection, col_selection = item

        if isinstance(row_selection, int):
            row_selection = [row_selection]
        # df[df['a'] < 10, 'b']
        elif isinstance(row_selection, DataFrame):
            if row_selection.shape[1] != 1:
                raise ValueError('Can only pass a one column DataFrame for selection')
            row_selection = next(iter(row_selection._data.values()))
            if row_selection.dtype.kind != 'b':
                raise TypeError('DataFrame must be a boolean')
            elif not isinstance(row_selection, (list, slice)):
                raise TypeError('Row selection must be either an int, slice, list, or DataFrame')
        

        if isinstance(col_selection, int):
            col_selection = [self.columns[col_selection]]
        elif isinstance(col_selection, str):
            col_selection = [col_selection]
        elif isinstance(col_selection, list):
            new_col_selection = []
            for col in col_selection:
                if isinstance(col, int):
                    # converting col to string
                    new_col_selection.append(self.columns[col])
                else:
                    # assuming col is a string
                    new_col_selection.append(col)
            col_selection = new_col_selection
        elif isinstance(col_selection, slice):
            start = col_selection.start
            stop = col_selection.stop
            step = col_selection.step

            if isinstance(start, str):
                start = self.columns.index(start)
            
            if isinstance(stop, str):
                # added 1 to include the last column
                stop = self.columns.index(stop) + 1
            
            # if isinstance(step, int):
            #     raise TypeError('step must be of type integer')
            col_selection = self.columns[start:stop:step]
        else:
            raise TypeError('column selection must be either int, string, list or slice')

        new_data = {}
        for col in col_selection:
            new_data[col] = self._data[col][row_selection]
        
        return DataFrame(new_data)

    def _ipython_key_completions_(self):
        # allows for tab completion when doing df['c
        return self.columns

    def __setitem__(self, key, value):
        # add a new column or overwrite an exisiting column
        if not isinstance(key, str):
            raise NotImplementedError('Can only set a single column')

        if isinstance(value, np.ndarray):
            if value.ndim != 1:
                raise ValueError('The setting array must be one dimensional')
            if len(value) != len(self):
                raise ValueError('Setting array must be of the same length as the DataFrame')
        elif isinstance(value, DataFrame):
            if value.shape[1] != 1:
                raise ValueError('Setting DataFrame must be one column')
            if len(value) != len(self):
                raise ValueError('Setting and Calling DataFrames must be the same length')
            # reassign value to the underlying numpy array of the column.
            value = next(iter(value._data.values()))
        elif isinstance(value, (int, str, bool, float)):
            value = np.repeat(value, len(self))
        else:
            raise TypeError('Setting value must either be a NumPy array, DataFrame, integer, string, float, or boolean')

        if value.dtype.kind == 'U':
            value = value.astype('O')
        
        self._data[key] = value

    def head(self, n=5):
        """
        Return the first n rows

        Parameters
        ----------
        n: int

        Returns
        -------
        DataFrame
        """
        return self[:n, :]

    def tail(self, n=5):
        """
        Return the last n rows

        Parameters
        ----------
        n: int

        Returns
        -------
        DataFrame
        """
        return self[-n:, :]

    ### Aggregation Methods ###

    def min(self):
        return self._agg(np.min)

    def max(self):
        return self._agg(np.max)

    def mean(self):
        return self._agg(np.mean)

    def median(self):
        return self._agg(np.median)

    def sum(self):
        return self._agg(np.sum)

    def var(self):
        return self._agg(np.var)

    def std(self):
        return self._agg(np.std)

    def all(self):
        return self._agg(np.all)

    def any(self):
        return self._agg(np.any)

    def argmax(self):
        return self._agg(np.argmax)

    def argmin(self):
        return self._agg(np.argmin)

    def _agg(self, aggfunc):
        """
        Generic aggregation function that applies the aggregation to each column

        Parameters
        ---------
        aggfunc: str of the aggregation function name in NumPy

        Returns
        -------
        DataFrame
        """
        new_data = {}
        for col, value in self._data.items():
            try: 
                new_data[col] = np.array([aggfunc(value)])
            except TypeError:
                pass
        return DataFrame(new_data)

    def isna(self):
        """
        Determines whether each value in the DataFrame is missing or not

        Returns
        -------
        A DataFrame of booleans the same size as the calling DataFrame
        """
        new_data = {}
        for col, value in self._data.items():
            kind = value.dtype.kind
            if kind == 'O':
                new_data[col] = value == None
            else:
                new_data[col] = np.isnan(value)
        return DataFrame(new_data)

    def count(self):
        """
        Counts the number of non-missing values per column

        Returns
        -------
        DataFrame
        """
        new_data = {}
        df = self.isna()
        length = len(df)        
        for col, value in df._data.items():
            val = length - value.sum()
            new_data[col] = np.array([val])
        return DataFrame(new_data)

    # In Pandas, only series have unique method, not DataFrames
    def unique(self):
        """
        Find the unique values of each column

        Returns
        -------
        A list of one-column DataFrames
        """
        # @ToDo: Cover the case for missing values in strings
        dfs = []
        for col, value in self._data.items():
            new_data = {col: np.unique(value)}
            dfs.append(DataFrame(new_data))
        if len(dfs) == 1:
            return dfs[0]
        return dfs

    def nunique(self):
        """
        Find the number of unique values in each column

        Returns
        -------
        A DataFrame
        """
        new_data = {}
        for col, value in self._data.items():
            new_data[col] = np.array([len(np.unique(value))])
        return DataFrame(new_data)

    def value_counts(self, normalize=False):
        """
        Returns the frequency of each unique value for each column

        Parameters
        ----------
        normalize: bool
        If True, returns the relative frequencies(percent)

        Returns
        -------
        A list of DataFrames or a single DataFrame if one column
        """
        dfs = []
        for col, value in self._data.items():
            uniques, raw_counts = np.unique(value, return_counts=True)

            # Sort counts from greatest to lowest
            order = np.argsort(-raw_counts)
            uniques = uniques[order]
            raw_counts = raw_counts[order]

            if normalize:
                raw_counts = raw_counts / raw_counts.sum()
            df = DataFrame({col: uniques, 'count': raw_counts })
            dfs.append(df)
        if len(dfs) == 1:
            return dfs[0]
        return dfs

    def rename(self, columns):
        """
        Renames columns in the DataFrame

        Parameters
        ----------
        columns: dict 
            A dictionary mapping the old column name to the new column name
        Returns
        -------
        A DataFrame
        """
        if not isinstance(columns, dict):
            raise TypeError('`columns` must be a dictionary')
        new_data = {}
        for col, value in self._data.items():
            new_col = columns.get(col, col)
            new_data[new_col] = value
        return DataFrame(new_data)

    def drop(self, columns):
        """
        Drops one or more columns from a DataFrame

        Parameters
        ----------
        columns: str or list of strings

        Returns
        -------
        A DataFrame
        """
        if isinstance(columns, str):
            columns = [columns]
        elif not isinstance(columns, list):
            raise TypeError('`columns` must be either a string or list')
        new_data = {}
        for col, value in self._data.items():
            if not col in columns:
                new_data[col] = value
        return DataFrame(new_data)


        









