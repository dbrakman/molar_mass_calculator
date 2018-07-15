import unittest
from  molar_mass_calculator import molar_mass_calculator as mmc

def percent_error(observed, actual):
    return (observed - actual)/actual


class MolarMassTester(unittest.TestCase):
    """
    Tests for sensibile behavior, using data from https://www.lfd.uci.edu/~gohlke/molmass/
    """
    ERR_THRESHOLD = .001 / 100  # tolerate up to .001 percent error

    def test_single_caps(self):
        """
        Find the molar mass of an element whose name is a single letter
        H: 1.008
        """
        result_h = mmc.find_molar_mass('H')
        actual_h = 1.008
        self.assertTrue(abs(percent_error(result_h, actual_h)) < .00001)

    def test_single_mixed_case(self):
        result = mmc.find_molar_mass('He')
        actual = 4.00
        self.assertTrue(abs(percent_error(result, actual)) < .00001)

    def test_multi_no_parens(self):
        result = mmc.find_molar_mass('C6H12O6')
        actual = 180.1559
        self.assertTrue(abs(percent_error(result, actual)) < .00001)

    def test_multi_parens(self):
        result = mmc.find_molar_mass('((PC5H10O8)2(C5H5N5)(C5H6N2O3))1000')
        actual = 735443.2
        self.assertTrue(abs(percent_error(result, actual)) < .00001)


if '__main__' == __name__:
    unittest.main()
