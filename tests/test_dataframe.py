import numpy as np
from numpy.testing import assert_array_equal
from tests import assert_df_equals
import pytest
import ickle as ick

pytestmark = pytest.mark.filterwarnings('ignore')

a = np.array(['a', 'b', 'c'])
b = np.array(['c', 'd', None])
c = np.random.rand(3)
d = np.array([True, False, True])
e = np.array([1, 2, 3])

df = ick.DataFrame({'a': a, 'b': b, 'c': c, 'd': d, 'e': e})

class TestDataFrameCreation:
    def test_input_types(self):
        with pytest.raises(TypeError):
            ick.DataFrame([1, 2, 3])

        with pytest.raises(TypeError):
            ick.DataFrame({1: 5, 'b': 10})

        with pytest.raises(TypeError):
            ick.DataFrame({'a': np.array([1]), 'b': 10})

        with pytest.raises(ValueError):
            ick.DataFrame({'a': np.array([1]),
                           'b': np.array([[1]])})

        # Correct construction of the dataframe. No errors.
        ick.DataFrame({
            'a': np.array([1]),
            'b': np.array([100])
        })

    def test_array_length(self):
        with pytest.raises(ValueError):
            ick.DataFrame({'a': np.array([1, 2]),
                           'b': np.array([1])})

        # Correct construction. No errors.
        ick.DataFrame({'a': np.array([1, 2]),
                       'b': np.array([5, 10])})

    def test_unicode_to_object(self):
        a_object = a.astype('O')
        assert_array_equal(df._data['a'], a_object)
        assert_array_equal(df._data['b'], b)
        assert_array_equal(df._data['c'], c)
        assert_array_equal(df._data['d'], d)
        assert_array_equal(df._data['e'], e)

    def test_len(self):
        # The assert keyword lets you test if a condition in your code returns True.
        # If not, the program will raise an AssertionError.
        assert len(df) == 3

    def test_columns(self):
        assert df.columns == ['a', 'b', 'c', 'd', 'e']

    def test_set_columns(self):
        with pytest.raises(TypeError):
            df.columns = 5

        with pytest.raises(ValueError):
            df.columns = ['a', 'b']

        with pytest.raises(TypeError):
            df.columns = [1, 2, 3, 4, 5]

        with pytest.raises(ValueError):
            df.columns = ['f', 'f', 'g', 'h', 'i']

        df.columns = ['f', 'g', 'h', 'i', 'j']
        assert df.columns == ['f', 'g', 'h', 'i', 'j']

        # set it back
        df.columns = ['a', 'b', 'c', 'd', 'e']
        assert df.columns == ['a', 'b', 'c', 'd', 'e']

    def test_shape(self):
        assert df.shape == (3, 5)

    def test_values(self):
        values = np.column_stack((a, b, c, d, e))
        assert_array_equal(df.values, values)

    def test_dtypes(self):
        cols = np.array(['a', 'b', 'c', 'd', 'e'], dtype='O')
        dtypes = np.array(
            ['string', 'string', 'float', 'bool', 'int'], dtype='O')

        df_result = df.dtypes
        df_answer = ick.DataFrame({'Column Name': cols, 'Data Type': dtypes})

        assert_df_equals(df_result, df_answer)


class TestSelection:
    def test_one_column(self):
        assert_array_equal(df['a'].values[:, 0], a)
        assert_array_equal(df['c'].values[:, 0], c)

    def test_multiple_columns(self):
        cols = ['a', 'b']
        df_result = df[cols]
        df_answer = ick.DataFrame({'a': a, 'b': b})
        assert_df_equals(df_result, df_answer)

    def test_simple_boolean(self):
        bool_arr = np.array([True, False, False])
        df_bool = ick.DataFrame({'col': bool_arr})
        df_result = df[df_bool]
        df_answer = ick.DataFrame({'a': a[bool_arr], 'b': b[bool_arr], 
        'c': c[bool_arr], 'd': d[bool_arr], 'e': e[bool_arr]})
        assert_df_equals(df_result, df_answer)

        with pytest.raises(ValueError):
            df_bool = ick.DataFrame({'col': bool_arr, 'col2': bool_arr})
            df[df_bool]

        with pytest.raises(TypeError):
            df_bool = ick.DataFrame({'col': np.array[1,2,3]})

    def test_one_column_tuple(self):
        assert_df_equals(df[:, 'a'], ick.DataFrame({'a': a}))

    def test_multiple_columns_tuple(self):
        cols = ['a', 'c']
        df_result = df[:, cols]
        df_answer = ick.DataFrame({'a': a, 'c': c})
        assert_df_equals(df_result, df_answer)

    def test_int_selection(self):
        assert_df_equals(df[:, 3], ick.DataFrame({'d': d}))

    def test_simultaneous_tuple(self):
        with pytest.raises(TypeError):
            s = set()
            df[s]

        with pytest.raises(ValueError):
            df[1, 2, 3]

    # @ToDo: Write tests for single element, all row selections, list columns, column slices
    
    def test_tab_complete(self):
        assert ['a', 'b', 'c', 'd', 'e'] == df._ipython_key_completions_()
    
    # TO-DO 
    def test_new_column(self):
        pass

    def test_head_tails(self):
        df_result = df.head(2)
        df_answer = ick.DataFrame({'a': a[:2], 'b': b[:2], 'c': c[:2], 'd': d[:2], 'e': e[:2]})
        assert_df_equals(df_result, df_answer)

        df_result = df.tail(2)
        df_answer = ick.DataFrame({'a': a[-2:], 'b': b[-2:], 'c': c[-2:], 'd': d[-2:], 'e': e[-2:]})
        assert_df_equals(df_result, df_answer)


a1 = np.array(['a', 'b', 'c'])
b1 = np.array([21, 15, 6])
c1 = np.array([4.3, np.nan, 9.1])
df1 = ick.DataFrame({'a': a1, 'b': b1, 'c': c1})

class TestAggregation:

    def test_min(self):
        df_result = df1.min()
        df_answer = ick.DataFrame({'a': np.array(['a'], dtype='O'), 'b': np.array([6]), 'c': np.array([np.nan])})
        assert_df_equals(df_result, df_answer)

