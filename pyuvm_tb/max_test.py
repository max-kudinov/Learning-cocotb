import pyuvm
from pyuvm import uvm_factory, uvm_test
from alu_env import AluEnv
from max_tester import MaxTester
from base_tester import BaseTester


@pyuvm.test()
class MaxTest(uvm_test):
    """Run with max operators"""

    def build_phase(self):
        uvm_factory().set_type_override_by_type(BaseTester, MaxTester)
        self.env = AluEnv("env", self)
