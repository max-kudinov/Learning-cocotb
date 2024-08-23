from pyuvm import uvm_root, uvm_sequence
from alu_seq_item import AluSeqItem
import sys

sys.path.insert(0, "..")
from tinyalu_utils import Ops  # noqa: E402


class FibonacciSeq(uvm_sequence):
    async def body(self):
        prev_num = 0
        cur_num = 1
        fib_list = [prev_num, cur_num]
        cmd = AluSeqItem("cmd", None, None, Ops.ADD)

        for _ in range(7):
            await self.start_item(cmd)
            cmd.A = prev_num
            cmd.B = cur_num
            await self.finish_item(cmd)
            fib_list.append(cmd.result)
            prev_num = cur_num
            cur_num = cmd.result

        uvm_root().logger.info("Fibonacci Sequence: " + str(fib_list))
