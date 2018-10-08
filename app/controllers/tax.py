from models.tax import TaxModel


class TaxController:
    def __init__(self):
        self.tax_codes = {
            '1': {'type': 'Food & Beverage', 'refundable': True},
            '2': {'type': 'Tobacco', 'refundable': False},
            '3': {'type': 'Entertainment', 'refundable': False},
        }
        self.model = TaxModel()

    def fetch(self):
        try:

            list_tax = self.model.select().fetchall

            data = []
            summary = {'price_subtotal': 0, 'tax_subtotal': 0, 'grand_total': 0}
            for tax in list_tax:

                tax_code = tax['tax_code']
                tax_price = tax['price']
                tax_code_data = self.tax_codes[str(tax_code)]

                single = {
                    'name': tax['name'],
                    'tax_code': tax_code,
                    'type': tax_code_data['type'],
                    'refundable': tax_code_data['refundable'],
                    'price': tax_price,
                }

                tax_value = self.calculate_tax(tax_code, tax_price)

                amount = tax_price + tax_value

                single['tax'] = tax_value
                single['amount'] = amount

                data.append(single)

                summary['price_subtotal'] += tax_price
                summary['tax_subtotal'] += tax_value
                summary['grand_total'] += amount

            return {'status': 1, 'result': data, 'summary': summary}

        except Exception as e:
            return {'status': 0, 'message': str(e)}

    def calculate_tax(self, tax_code, tax_price):
        try:
            if type(tax_code) is str or type(tax_price) is str:
                raise TypeError("Input should be a integer")

            if str(tax_code) not in self.tax_codes:
                raise Exception('Tax code wrong')

            if tax_price < 0:
                raise Exception("Tax price cannot minus")

            if tax_code == 1:
                # 10% of price
                tax_value = 10 / 100 * tax_price
            elif tax_code == 2:
                # 10 + (2% of price)
                tax_value = 10 + (2 / 100 * tax_price)
            else:
                # price < 100 free, price >= 100 : 1% of (price - 100)
                tax_value = 0 if tax_price < 100 else 1 / 100 * (tax_price - 100)
            return tax_value
        except Exception:
            raise

    def insert(self, data):
        try:
            self.validation(data)

            status = self.model.insert(data).status
            result = {'status': status, 'result': 'Success'}
            return result
        except Exception as e:
            return {'status': 0, 'message': str(e)}

    def validation(self, data):
        try:
            allowed_field = ['name', 'tax_code', 'price']
            for field, value in data.items():
                if not value:
                    raise Exception('Sorry field {} is mandatory'.format(', '.join(allowed_field)))

                if field not in allowed_field:
                    raise Exception('Sorry only field {} are allowed'.format(', '.join(allowed_field)))
            if len(data) != 3:
                raise Exception('Sorry field {} is mandatory'.format(', '.join(allowed_field)))
            if str(data['tax_code']) not in self.tax_codes:
                raise Exception('Sorry your tax code wrong')
        except Exception:
            raise
