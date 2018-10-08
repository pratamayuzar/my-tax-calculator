import unittest
from controllers.tax import TaxController


class Test(unittest.TestCase):
    def setUp(self):
        self.tax = TaxController()

    def test_tax_code1(self):
        """
        Test for tax code 1 returns the correct tax
        """
        result = self.tax.calculate_tax(1, 1000)
        self.assertEqual(result, 100)

    def test_tax_code2(self):
        """
        Test for tax code 2 returns the correct tax
        """
        result = self.tax.calculate_tax(2, 1000)
        self.assertEqual(result, 30)

    def test_tax_code3(self):
        """
        Test for tax code 3 returns the correct tax
        """
        result = self.tax.calculate_tax(3, 150)
        self.assertEqual(result, 0.5)

    def test_tax_code4(self):
        """
        Test for tax code 4 returns raise Tax code wrong
        """
        with self.assertRaises(Exception) as context:
            self.tax.calculate_tax(4, 1000)

        self.assertTrue('Tax code wrong' in str(context.exception))

    def test_tax_code_string(self):
        """
        Test for tax code 3 string returns raise Input should be a integer
        """
        with self.assertRaises(Exception) as context:
            self.tax.calculate_tax('3', 1000)

        self.assertTrue('Input should be a integer' in str(context.exception))

    def test_tax_price_minus(self):
        """
        Test for tax price minus returns raise Tax price cannot minus
        """
        with self.assertRaises(Exception) as context:
            self.tax.calculate_tax(3, -1000)

        self.assertTrue('Tax price cannot minus' in str(context.exception))

    def test_tax_price_string(self):
        """
        Test for tax price string returns raise Input should be a integer
        """
        with self.assertRaises(Exception) as context:
            self.tax.calculate_tax(3, '1000')

        self.assertTrue('Input should be a integer' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
