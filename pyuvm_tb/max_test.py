import pyuvm
from pyuvm import uvm_factory
from base_test import BaseTest
from base_seq import BaseSeq
from seq import MaxSeq


@pyuvm.test()
class MaxTest(BaseTest):
    """Run with max operators"""

    def start_of_simulation_phase(self):
        uvm_factory().set_type_override_by_type(BaseSeq, MaxSeq)
