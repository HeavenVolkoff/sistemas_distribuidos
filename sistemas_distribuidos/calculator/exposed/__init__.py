# Standard
from functools import reduce
import typing as T
import operator


def add(*args: T.Any) -> T.Any:
    return reduce(operator.add, args, 0)


def sub(*args: T.Any) -> T.Any:
    return reduce(operator.sub, args, 0)


def mul(*args: T.Any) -> T.Any:
    return reduce(operator.mul, args, 1)


def div(*args: T.Any) -> T.Any:
    return reduce(operator.truediv, args, 1)
