import unittest
from find_missing import *


class FindMissingTests(unittest.TestCase):

    def test_calc_diff(self):
        #TODO: perhaps calc_diff function should be determining ascending or descending state?
        self.assertEqual(calc_diff(1, 20, -1), 21)
        self.assertEqual(calc_diff(1, 20, 0), 20)
        self.assertEqual(calc_diff(1, 20, 20), 0)
        self.assertEqual(calc_diff(1, 20, 19), 1)
        self.assertEqual(calc_diff(1, 20, 21), -1)
        self.assertEqual(calc_diff(0, 20, -1), 21)
        self.assertEqual(calc_diff(-1, 20, -1), -21)

    def test_get_specified_num(self):
        line = "1krMK432WG2CaFbiNnyBewaksT09he5   DSC003.103   bin    1.1 GB   2018-06-12 20:54:22"
        pattern = re.compile("DSC003\.(\d+)")
        self.assertEqual(get_specified_num(pattern, line), 103)

        line = "1krMK432WG2CaFbiNnyBewaksT09he5   DSC003.103   bin    1.1 GB   2018-06-12 20:54:22"
        pattern = re.compile("DSC003\.\d+")
        self.assertRaises(AttributeError, get_specified_num, pattern, line)

        line = "1krMK432WG2CaFbiNnyBewaksT09he5   DSC003.aa   bin    1.1 GB   2018-06-12 20:54:22"
        pattern = re.compile("DSC003\.(\d+)")
        self.assertIsNone(get_specified_num(pattern, line))

        line = "1krMK432WG2CaFbiNnyBewaksT09he5   DSC003.aa   bin    1.1 GB   2018-06-12 20:54:22"
        pattern = re.compile("(DSC)003\.")
        self.assertRaises(ValueError, get_specified_num, pattern, line)


if __name__ == '__main__':
    unittest.main()
