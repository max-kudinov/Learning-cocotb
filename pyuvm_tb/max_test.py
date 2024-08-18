import pyuvm
from base_test import BaseTest
from max_tester import MaxTester


@pyuvm.test()
class MaxTest(BaseTest):
    """Run with max operators"""
    def build_phase(self):
        self.tester = MaxTester()
