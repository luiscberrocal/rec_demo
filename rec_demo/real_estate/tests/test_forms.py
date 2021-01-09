import re

from django.test import SimpleTestCase

from rec_demo.real_estate.forms import ContractForm


class TestRegexpExtraction(SimpleTestCase):

    def test_regexp(self):
        regexp_str = ContractForm.REAL_ESTATE_SPACE_PATTERN[:-2] + r'(\d+)'
        reg = re.compile(regexp_str)
        test_str = 'real_estate_space_2'
        match = reg.match(test_str)
        if match:
            self.assertEqual(match.group(1), '2')
        else:
            self.fail('Did not work')

    def test_merge_dict(self):
        y = {'name': 'Luis', 'last_name': 'Berrocal'}
        x = {'middle_name': 'Carlos'}

        y = {**y, **x}
        self.assertEqual(y['middle_name'], 'Carlos')
        self.assertEqual(y['last_name'], 'Berrocal')

        y = {**y, 'last_name': 'Wayne'}
        self.assertEqual(y['last_name'], 'Wayne')

