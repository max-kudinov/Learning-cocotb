import cocotb
from tinyalu_utils import TinyAluBfm, Ops, alu_prediction, logger


class Scoreboard():
    def __init__(self):
        self.bfm = TinyAluBfm()
        self.cmds = list()
        self.results = list()
        self.cvg = set()

    async def get_cmd(self):
        while True:
            cmd = await self.bfm.get_cmd()
            self.cmds.append(cmd)

    async def get_result(self):
        while True:
            result = await self.bfm.get_result()
            self.results.append(result)

    def start_tasks(self):
        cocotb.start_soon(self.get_cmd())
        cocotb.start_soon(self.get_result())

    def check_results(self):
        passed = True
        for cmd in self.cmds:
            a, b, op_int = cmd
            op = Ops(op_int)
            self.cvg.add(op)
            actual = self.results.pop(0)
            prediction = alu_prediction(a, b, op)
            if actual == prediction:
                logger.info(f"PASSED: {a:02x} {op.name} {b:02x} = "
                            f"{actual:04x}")
            else:
                logger.error(
                    f"FAILED: {a:02x} {op.name} {b:02x} = {actual:04x}"
                    f" - predicted {prediction:04x}")
                passed = False

        if len(set(Ops) - self.cvg) > 0:
            logger.error(
                f"Functional coverage error. Missed: {set(Ops) - self.cvg}")
            passed = False
        else:
            logger.info("Covered all operations")

        return passed
