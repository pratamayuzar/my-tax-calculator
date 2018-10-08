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

    def test_tax_insert(self):
        """
        Test for insert tax returns the success
        """
        data = {
            'name': 'Small Mac',
            'tax_code': 1,
            'price': 500
        }
        result = self.tax.insert(data)
        self.assertEqual(result, {'status': 1, 'result': 'Success'})

    def test_tax_insert_error_mandatory(self):
        """
        Test for insert tax returns the error mandatory
        """
        data = {
            'name': 'Small Mac',
            'tax_code': 1
        }
        result = self.tax.insert(data)
        self.assertEqual(result, {'message': 'Sorry field name, tax_code, price is mandatory', 'status': 0})

    def test_tax_insert_error_other_field(self):
        """
        Test for insert tax returns the error only allowed field
        """
        data = {
            'name': 'Small Mac',
            'tax_code': 1,
            'price': 500,
            'amount': 500
        }
        result = self.tax.insert(data)
        self.assertEqual(result, {'message': 'Sorry only field name, tax_code, price are allowed', 'status': 0})

    def test_tax_insert_error_tax_code(self):
        """
        Test for insert tax returns the error tax code wrong
        """
        data = {
            'name': 'Small Mac',
            'tax_code': 4,
            'price': 500
        }
        result = self.tax.insert(data)
        self.assertEqual(result, {'message': 'Sorry your tax code wrong', 'status': 0})


if __name__ == '__main__':
    unittest.main()
