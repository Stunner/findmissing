import unittest
import io
# import sys
from findmissing import *


class FindMissingTests(unittest.TestCase):

    def test_asc_or_desc_check(self):
        self.assertEqual(asc_or_desc_check(2, 3), 1)
        self.assertEqual(asc_or_desc_check(2, 3, 1), 1)
        self.assertRaises(Exception, asc_or_desc_check, 2, 3, -1)

        self.assertEqual(asc_or_desc_check(12, 9), -1)
        self.assertEqual(asc_or_desc_check(12, 9, -1), -1)
        self.assertRaises(Exception, asc_or_desc_check, 12, 9, 1)

        self.assertEqual(asc_or_desc_check(8, 8), -1)

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

    def test_calc_diff(self):
        #TODO: perhaps calc_diff function should be determining ascending or descending state?
        self.assertEqual(calc_diff(1, 20, -1), 21)
        self.assertEqual(calc_diff(1, 20, 0), 20)
        self.assertEqual(calc_diff(1, 20, 20), 0)
        self.assertEqual(calc_diff(1, 20, 19), 1)
        self.assertEqual(calc_diff(1, 20, 21), -1)
        self.assertEqual(calc_diff(0, 20, -1), 21)
        self.assertEqual(calc_diff(-1, 20, -1), -21)

    def test_print_diff(self):
        # reference: https://stackoverflow.com/a/34738440/347339
        captured_output = io.StringIO()  # Create StringIO object
        sys.stdout = captured_output  # and redirect stdout.
        print_diff(12, 1, 8, 0)  # Call function.
        output = "9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n"
        self.assertEqual(captured_output.getvalue(), output)
        sys.stdout = sys.__stdout__

        captured_output = io.StringIO()  # Create new StringIO object (required to reset previous value)
        sys.stdout = captured_output
        print_diff(5, -1, 8, 1)
        output = "7\n6\n5\n4\n"
        self.assertEqual(captured_output.getvalue(), output)
        sys.stdout = sys.__stdout__

    def test_main(self):
        with open('output1.txt', 'r') as content_file:
            captured_output = io.StringIO()
            sys.stdout = captured_output
            args = ['findmissing.py', '-f', 'findmissing_bug2.txt',
                    '-p', 'DSC003\\.(\\d+)', '-l', 'DSC003.199']
            main(args)
            self.assertEqual(captured_output.getvalue(), content_file.read())
            sys.stdout = sys.__stdout__

        with open('output2.txt', 'r') as content_file:
            captured_output = io.StringIO()
            sys.stdout = captured_output
            args = ['findmissing.py', '-f', 'findmissing_sample_tedious.txt',
                    '-p', 'DSC003\\.(\\d+)', '-l', 'DSC003.310']
            main(args)
            self.assertEqual(captured_output.getvalue(), content_file.read())
            sys.stdout = sys.__stdout__


if __name__ == '__main__':
    unittest.main()
