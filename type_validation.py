import pprint as pp


def check_tuple(x, args):
    specs = args[0]
    if not isinstance(x, tuple) or not len(x) == len(specs):
        return False
    for i, item in enumerate(x):
        if not check_type(item, specs[i]):
            return False
    return True


def check_list(x, args):
    itemspec = args[0]
    if not isinstance(x, list):
        return False
    for item in x:
        if not check_type(item, itemspec):
            return False
    return True


def check_and(x, args):
    specs = args[0]
    for s in specs:
        if not check_type(x, s):
            return False
    return True


name_to_checker = {list: check_list,
                   tuple: check_tuple,
                   "and": check_and}


def check_spec(x, spec):
    variant = spec[0]
    v = name_to_checker[variant](x, spec[1:])
    return v


def check_type(x, spec):
    v = False
    if isinstance(spec, type):
        v = isinstance(x, spec)
    elif isinstance(spec, tuple):
        check_spec(x, spec)
    elif callable(spec):
        v = spec(x)
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


def assert_type(x, spec):
    if not check_spec(x, spec):
        raise AssertionError(
            "Type assertion failed"
            + "\nExpected:\n"
            + fmt_spec(spec)
            + "\nGot:\n"
            + str(x))
