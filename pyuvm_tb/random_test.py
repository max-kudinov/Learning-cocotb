import pyuvm
from pyuvm import uvm_factory, uvm_test
from alu_env import AluEnv
from base_tester import BaseTester
from random_tester import RandomTester


@pyuvm.test()
class RandomTest(uvm_test):
    """Run with random operators"""

    def build_phase(self):
        uvm_factory().set_type_override_by_type(BaseTester, RandomTester)
        self.env = AluEnv("env", self)
