import cocotb
from cocotb.triggers import ClockCycles
from pyuvm import ConfigDB, uvm_test
from alu_env import AluEnv
from base_seq import BaseSeq


class BaseTest(uvm_test):
    def build_phase(self):
        self.env = AluEnv("env", self)

    def end_of_elaboration_phase(self):
        self.seqr = ConfigDB().get(self, "", "SEQR")

    async def run_phase(self):
        self.raise_objection()
        seq = BaseSeq.create("seq")
        await seq.start(self.seqr)
        await ClockCycles(cocotb.top.clk, 50)
        self.drop_objection()
