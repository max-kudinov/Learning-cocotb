from pyuvm import uvm_driver, uvm_get_port
import sys
sys.path.insert(0, "..")
from tinyalu_utils import TinyAluBfm  # noqa: E402


class Driver(uvm_driver):
    def build_phase(self):
        self.bfm = TinyAluBfm()
        self.gp = uvm_get_port("gp", self)

    async def run_phase(self):
        await self.bfm.reset()
        self.bfm.start_tasks()
        while True:
            a, b, op = await self.gp.get()
            await self.bfm.send_op(a, b, op)
