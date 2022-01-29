import pprint as pp
import re
import operator as op
from functools import partial


def check_tuple(x, args):
    specs = args[0]
    if not isinstance(x, tuple):
        return (False, "Not a tuple")
    if not len(x) == len(specs):
        return (False, f"Tuple of length {len(x)} should be length {len(specs)}")
    for i, item in enumerate(x):
        r = check_type(item, specs[i])
        if not r[0]:
            return r
    return (True,)


def check_list(x, args):
    itemspec = args[0]
    if not isinstance(x, list):
        return (False, "Not a list")
    for item in x:
        r = check_type(item, itemspec)
        if not r[0]:
            return r
    return (True,)


def check_and(x, args):
    specs = args[0]
    for s in specs:
        r = check_type(x, s)
        if not r[0]:
            return r
    return (True,)


name_to_checker = {list: check_list,
                   tuple: check_tuple,
                   "and": check_and}


def check_spec(x, spec):
    variant = spec[0]
    v = name_to_checker[variant](x, spec[1:])
    return v


def check_type(x, spec):
    v = None
    if isinstance(spec, type):
        v = (True,) if isinstance(x, spec) \
            else (False, f"Not of type {spec.__name__}")
    elif isinstance(spec, tuple):
        v = check_spec(x, spec)
    elif callable(spec):
        v = (True,) if spec(x) \
            else (False, f"Does not satisfy custom predicate: {spec}")
    else:
        raise Exception("Invalid type spec:\n" + str(spec))
    return v


def firstor(*args):
    for arg in args:
        if arg:
            return arg
    return args[-1]


def fmt_spec(spec, level=0):
    if isinstance(spec, type):
        return spec.__name__
    elif isinstance(spec, tuple):
        first = spec[0]
        first = first.__name__ if isinstance(first, type) else first
        ret = "(" + first
        level += 2
        for i, x in enumerate(spec[1:]):
            ret += "\n" + " " * level + fmt_spec(x, level=level)
        return ret + ")"
    elif callable(spec):
        return firstor(pp.pprint(spec), str(spec))
    elif isinstance(spec, list):
        ret = "[" + fmt_spec(spec[0])
        level += 1
        for s in spec[1:]:
            ret += "\n" + " " * level + fmt_spec(s, level=level)
        return ret + "]"
    else:
        return firstor(pp.pprint(spec), str(spec))


truncate_lines_re = re.compile(r"(?:[^\n]*\n?){,16}")


def assert_type(x, spec):
    result = check_spec(x, spec)
    if not result[0]:
        msg = result[1]
        msg = "" if msg is None else "\n" + msg
        raw_x_str = str(x)
        x_str = truncate_lines_re.match(raw_x_str).group()
        if len(x_str) < len(raw_x_str):
            x_str += "\n... <TRUNCATED>"
        raise AssertionError(
            "Type assertion failed"
            + msg
            + "\nExpected:\n"
            + fmt_spec(spec)
            + "\nGot:\n"
            + x_str)


non_neg_p = partial(op.le, 0)
