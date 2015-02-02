from dask.threaded import get
from dask.async import inc
from dask.utils import raises
from operator import add


def test_get():
    dsk = {'x': 1, 'y': 2, 'z': (inc, 'x'), 'w': (add, 'z', 'y')}
    assert get(dsk, 'w') == 4
    assert get(dsk, ['w', 'z']) == (4, 2)


def test_nested_get():
    dsk = {'x': 1, 'y': 2, 'a': (add, 'x', 'y'), 'b': (sum, ['x', 'y'])}
    assert get(dsk, ['a', 'b']) == (3, 3)


def bad(x):
    raise ValueError()

def test_exceptions_rise_to_top():
    dsk = {'x': 1, 'y': (bad, 'x')}
    assert raises(ValueError, lambda: get(dsk, 'y'))