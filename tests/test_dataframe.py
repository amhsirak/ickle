import numpy as np
from numpy.testing import assert_array_equal
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

        # Correct constuction of the dataframe. No errors.
        ick.DataFrame({
                'a': np.array([1]), 
                'b': np.array([100])
            })
    
    def test_array_length(self):
        with pytest.raises(ValueError):
            ick.DataFrame({'a': np.array([1,2]),
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
        # The assert keyword lets you test if a condition in your code returns True, if not, the program will raise an AssertionError.
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