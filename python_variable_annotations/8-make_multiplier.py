#!/usr/bin/env python3
"""Module that provides a multiplier function."""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Return a function that multiplies a float by multiplier."""
    def multiply(number: float) -> float:
        return number * multiplier

    return multiply
