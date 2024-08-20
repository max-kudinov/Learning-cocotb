import pyuvm
from pyuvm import uvm_test
from random_env import RandomEnv


@pyuvm.test()
class RandomTest(uvm_test):
    """Run with random operators"""

    def build_phase(self):
        self.env = RandomEnv("env", self)
