import pyuvm
from base_test import BaseTest
from random_tester import RandomTester


@pyuvm.test()
class RandomTest(BaseTest):
    """Run with random operators"""
    def build_phase(self):
        self.tester = RandomTester()
