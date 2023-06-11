<h1 align="center"> 📈 Ickle - Data Analysis Library</h1>

<h3 align="center">
  A tiny DataFrame, statistics and analysis library for Python
</h3>

<div align="center">

[![PyPI version](https://badge.fury.io/py/ickle.svg)](https://badge.fury.io/py/ickle)
[![Downloads](https://static.pepy.tech/personalized-badge/ickle?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/ickle)
[![Package Status](https://img.shields.io/static/v1?label=status&message=stable&color=brightgreen)](https://pypi.org/project/ickle/)
  
</div>

## Installation

Ickle can be installed via pip through PyPi

```
pip install ickle
```

## Features
- [x]  DataFrame along with Visual Representation
- [x]  Basic properties (len, columns, shape, etc)
- [x]  Subset Selection
- [x]  Basic Methods (head, tail)
- [x]  Aggregation Methods (min, max, median, sum, etc)
- [x]  Non-Aggregation Methods (abs, copy, clip, cummin, etc)
- [x]  Additional Methods (isna, count, unique, etc)
- [x]  String-Only Methods (capitalize, center, count, find, etc)
- [x]  Pivot Table
- [ ]  CSV
    - [x]  read_csv
    - [ ]  to_csv
- [ ]  Excel
    - [x]  read_excel
    - [ ]  to_excel
    
... and more. 🚀 Checkout [PATH.md](PATH.md) to see the roadmap.

## How To Contribute?
See [CONTRIBUTION.md](CONTRIBUTION.md) to know more.

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

## Documentation

Read the documentation <a href="https://nbviewer.org/github/karishmashuklaa/ickle/blob/master/Ickle%20Documentation.ipynb">here</a>

## Authors
<a href="https://github.com/karishmashuklaa">@karishmashuklaa</a>

<a href="https://github.com/psy-pri">@psy-pri</a>
