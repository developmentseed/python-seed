"""
pyseed.app
====

This is from the file docstring.
"""


def dup_strings(arg_one: str, arg_two: int):
    """
    Return a repeated string. This is the main function docstring.

    Parameters
    ----------

    arg_one
        A string that should be repeated.

    arg_two
        A integer of the number of times `arg_one` should be repeated.

    >>> dup_strings('A', 3)
    'AAA'
    """
    return arg_one * arg_two


class Pizza:
    """A delicious object."""

    def __init__(self, size: int = 16):
        """
        Initialize pizzas with a size.

        Parameters
        ----------

        size
            Diameter in inchs.

        """
        self.size = size
        self.cheese = False

    def add_cheese(self):
        """
        Adds cheese.

        >>> pizza = Pizza()
        >>> pizza.cheese
        False
        >>> pizza.add_cheese()
        >>> pizza.cheese
        True

        """
        self.cheese = True
