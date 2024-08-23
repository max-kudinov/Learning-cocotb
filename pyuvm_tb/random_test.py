import pyuvm
from pyuvm import uvm_factory
from base_test import BaseTest
from base_seq import BaseSeq
from seq import RandomSeq


@pyuvm.test()
class RandomTest(BaseTest):
    """Run with random operators"""

    def start_of_simulation_phase(self):
        uvm_factory().set_type_override_by_type(BaseSeq, RandomSeq)
