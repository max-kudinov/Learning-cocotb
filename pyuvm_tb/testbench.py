import cocotb
from cocotb.triggers import Combine
import pyuvm
from pyuvm import CRITICAL, uvm_factory, uvm_sequence, uvm_test, ConfigDB
from alu_env import AluEnv
from fibonacci_seq import FibonacciSeq
from seq import RandomSeq, MaxSeq


class AluTest(uvm_test):
    def build_phase(self):
        self.env = AluEnv("env", self)

    def end_of_elaboration_phase(self):
        self.test_all = TestAllSeq.create("test_all")

    async def run_phase(self):
        self.raise_objection()
        await self.test_all.start()
        self.drop_objection()


class TestAllSeq(uvm_sequence):
    async def body(self):
        seqr = ConfigDB().get(None, "", "SEQR")
        rand_seq = RandomSeq("random")
        max_seq = MaxSeq("max")
        await rand_seq.start(seqr)
        await max_seq.start(seqr)


@pyuvm.test()
class FibonacciTest(AluTest):
    def end_of_elaboration_phase(self):
        ConfigDB().set(None, "*", "DISABLE_COVERAGE_ERRORS", True)
        self.env.set_logging_level_hier(CRITICAL)
        uvm_factory().set_type_override_by_type(TestAllSeq, FibonacciSeq)
        return super().end_of_elaboration_phase()
