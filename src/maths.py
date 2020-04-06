class Maths:
    def addition(value1, value2):
        """Add 2 integer values. Raises `TypeError` if arguments are non-integer."""
        if not isinstance(value1, int) or not isinstance(value2, int):
            raise TypeError("Arguments must be integers")

        return value1 + value2
