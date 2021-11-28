import numpy as np
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

        # Correct constuction of the data frame. No errors.
        ick.DataFrame({
                'a': np.array([1]), 
                'b': np.array([100])
            })