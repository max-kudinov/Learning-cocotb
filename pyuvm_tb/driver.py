from pyuvm import uvm_analysis_port, uvm_driver
from alu_result_item import AluResultItem
import sys
sys.path.insert(0, "..")
from tinyalu_utils import TinyAluBfm  # noqa: E402


class Driver(uvm_driver):
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)

    def start_of_simulation_phase(self):
        self.bfm = TinyAluBfm()

    async def launch_tb(self):
        await self.bfm.reset()
        self.bfm.start_tasks()

    async def run_phase(self):
        await self.launch_tb()
        self.bfm.start_tasks()
        while True:
            cmd = await self.seq_item_port.get_next_item()
            await self.bfm.send_op(cmd.A, cmd.B, cmd.op)
            result = await self.bfm.get_result()
            self.ap.write(result)
            cmd.result = result
            self.seq_item_port.item_done()
