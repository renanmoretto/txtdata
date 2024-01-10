# Easy and light manager for basic text data.

TxtData is a Python library designed for basic handling of data in .txt files. This lightweight library, with less than 300 lines of code, offers an easy-to-use API and includes comprehensive, well-written tests.


- Simple and intuitive handling of .txt data.
- Lightweight design for efficient performance.
- Extensive testing ensuring reliability.

## Installation
```
pip install txtdata
```

## Examples
```python
from txtdata import TxtData

# Creating an empty TxtData instance
txt = TxtData()
print(txt.empty)  # Output: True

# Creating with a simple dictionary.
txt = TxtData({'A': [1,2,3], 'B': ['x','y','z']})
print(txt)  
# Output: [{'A': 1, 'B': 'x'}, {'A': 2, 'B': 'y'}, {'A': 3, 'B': 'z'}]

# Inserting data
txt = TxtData()
txt.insert({'A': 123, 'B': 'zzz'})  # single data by single dict
txt.insert(A=182, C='asdf')  # single data by keyword
txt.insert([{'A': None}, {'B': 'zzz', 'C': 'yes'}])  # multiple data by list of dicts
txt.insert({'A': [1, 3], 'B': ['yyy', 'www']})  # multiple data by dict of lists
print(txt)
# Output: [
#     {'A': 123, 'B': 'zzz', 'C': None},
#     {'A': 182, 'B': None, 'C': 'asdf'},
#     {'A': None, 'B': None, 'C': None},
#     {'A': None, 'B': 'zzz', 'C': 'yes'},
#     {'A': 1, 'B': 'yyy', 'C': None},
#     {'A': 3, 'B': 'www', 'C': None}
# ]

# Filtering data
filtered_txt = txt.filter(A=182)
print(len(filtered_txt))  # Output: 1 (based on data above)

# Delete
txt.delete(B=None) # Deletes all data with B equals to None

# Saving
txt.save('data.txt', delimiter=';')
# txt file:
# A;B;C
# 123;zzz;
# 182;;asdf
# ;;
# ;zzz;yes
# 1;yyy;
# 3;www;


```