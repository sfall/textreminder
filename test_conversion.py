import conversion
import unittest


class ConversionTestCase(unittest.TestCase):

    def test_convert(self):
        number = '1234567890'
        carrier = 'Sprint'
        target = conversion.convert(number, carrier)
        assert number in target
        assert 'sprintpcs' in target


if __name__ == '__main__':
    unittest.main()
