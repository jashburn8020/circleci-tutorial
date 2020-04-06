import unittest
from src.maths import Maths


class MathsTest(unittest.TestCase):
    """Tests for `maths.Maths`"""

    def test_addition(self):
        self.assertEqual(Maths.addition(2, 3), 5)

    def test_addition_first_arg_non_int(self):
        with self.assertRaises(TypeError):
            Maths.addition(1.1, 2)

    def test_addition_second_arg_non_int(self):
        with self.assertRaises(TypeError):
            Maths.addition(1, 2.1)

    def test_addition_both_args_non_int(self):
        with self.assertRaises(TypeError):
            Maths.addition(1.1, 2.1)
