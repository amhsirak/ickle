## 📈 Ickle - Data Analysis Library 
**A tiny data analysis library for common day-to-day analytical tasks. Written in Python, for Python.**

## Installation

Ickle can be installed via pip through PyPi

```
pip install ickle
```

## Getting Started

### DataFrame
A DataFrame holds two dimensional heterogenous data. It accepts dictionary as input, with Numpy arrays as values and strings as column names.

```py
import numpy as np
import ickle as ick

name = np.array(['John', 'Sam', 'Tina', 'Josh', 'Jack', 'Jill'])
place = np.array(['Kolkata', 'Mumbai', 'Delhi', 'Mumbai', 'Mumbai', 'Mumbai'])
weight = np.array([57, 70, 54, 59, 62, 70])
married = np.array([True, False, True, False, False, False])

data = {'name': name, 'place': place, 'weight': weight, 'married': married}
df = ick.DataFrame(data)
```

You can use *ickle* easily in <a href="https://jupyter.org/">Jupyter Notebooks</a>
## Documentation

Read the documentation <a href="https://nbviewer.org/github/karishmashuklaa/ickle/blob/master/Ickle%20Documentation.ipynb">here</a>

<hr />
Copyright 2022 <a href='https://github.com/karishmashuklaa/'>Karishma Shukla</a>

