from pyuvm import uvm_analysis_port, uvm_driver
import sys
sys.path.insert(0, "..")
from tinyalu_utils import TinyAluBfm  # noqa: E402


class Driver(uvm_driver):
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)

    def start_of_simulation_phase(self):
        self.bfm = TinyAluBfm()

    async def run_phase(self):
        await self.bfm.reset()
        self.bfm.start_tasks()
        while True:
            cmd = await self.seq_item_port.get_next_item()
            await self.bfm.send_op(cmd.A, cmd.B, cmd.op)
            self.seq_item_port.item_done()
