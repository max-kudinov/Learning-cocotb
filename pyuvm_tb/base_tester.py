import cocotb
from cocotb.triggers import ClockCycles
from pyuvm import uvm_component, uvm_put_port
import sys
sys.path.insert(0, "..")
from tinyalu_utils import TinyAluBfm, Ops  # noqa: E402


class BaseTester(uvm_component):
    """Gets operands, commands and sends them"""

    def get_operands(self):
        raise RuntimeError("You must extend BaseTester and override"
                           "get_operands().")

    def build_phase(self):
        self.pp = uvm_put_port("pp", self)

    async def run_phase(self):
        self.raise_objection()
        self.bfm = TinyAluBfm()
        ops = list(Ops)

        for op in ops:
            a, b = self.get_operands()
            cmd_tupple = (a, b, op)
            await self.pp.put(cmd_tupple)

        await ClockCycles(signal=cocotb.top.clk, num_cycles=10, rising=False)
        self.drop_objection()
