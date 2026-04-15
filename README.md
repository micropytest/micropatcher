# *micro:Patcher*

A lightweight lib for patching things on **micro:Pytest** and **MicroPython**.


## Install

```bash
micropython -m mip install github:micropytest/micropatcher
```


## Usage

```python
from micropatcher import Patcher

patcher = Patcher()
```

### Attribute patching

```python
p = Point(x=12, y=34)
patcher.setattr(p, "x", 21)
```

### Item patching

```python
d = dict(x=12, y=34)
patcher.setitem(d, "x", 21)
patcher.delitem(d, "x)
```

### Undoing the patching

```python
patcher.undo()
```
