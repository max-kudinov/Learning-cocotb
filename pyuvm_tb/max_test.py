import pyuvm
from pyuvm import uvm_test
from max_env import MaxEnv


@pyuvm.test()
class MaxTest(uvm_test):
    """Run with max operators"""

    def build_phase(self):
        self.env = MaxEnv("env", self)
