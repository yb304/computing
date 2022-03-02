from functools import partial
import operator as op

non_neg_p = partial(op.le, 0)
non_empty_str_spec = ("and", [str, (lambda x: x)])
nat_int_p = ("and", [int, non_neg_p])


rel_level_p = ("and", [float])
