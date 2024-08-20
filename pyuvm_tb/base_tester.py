from pyuvm import uvm_component
from tinyalu_utils import TinyAluBfm, Ops


class BaseTester(uvm_component):
    """Gets operands, commands and sends them"""

    def start_of_simulation_phase(self):
        TinyAluBfm().start_tasks()

    async def run_phase(self):
        self.raise_objection()
        self.bfm = TinyAluBfm()
        ops = list(Ops)

        for op in ops:
            a, b = self.get_operands()
            await self.bfm.send_op(a, b, op)

        await self.bfm.send_op(0, 0, 1)
        await self.bfm.send_op(0, 0, 1)
        self.drop_objection()
