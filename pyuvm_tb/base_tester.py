from tinyalu_utils import TinyAluBfm, Ops


class BaseTester():
    """Gets operands, commands and sends them"""

    async def execute(self):
        self.bfm = TinyAluBfm()
        ops = list(Ops)

        for op in ops:
            a, b = self.get_operands()
            await self.bfm.send_op(a, b, op)

        await self.bfm.send_op(0, 0, 1)
        await self.bfm.send_op(0, 0, 1)
