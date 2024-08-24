from pyuvm import ConfigDB, uvm_root, uvm_sequence
from alu_seq_item import AluSeqItem
import sys

from op_seq import OpSeq
sys.path.insert(0, "..")
from tinyalu_utils import Ops  # noqa: E402


async def do_add(seqr, a, b):
    seq = OpSeq("seq", a, b, Ops.ADD)
    await seq.start(seqr)
    return seq.result


async def do_and(seqr, a, b):
    seq = OpSeq("seq", a, b, Ops.AND)
    await seq.start(seqr)
    return seq.result


async def do_xor(seqr, a, b):
    seq = OpSeq("seq", a, b, Ops.XOR)
    await seq.start(seqr)
    return seq.result


async def do_mul(seqr, a, b):
    seq = OpSeq("seq", a, b, Ops.MUL)
    await seq.start(seqr)
    return seq.result


class FibonacciSeq(uvm_sequence):
    def __init__(self, name):
        super().__init__(name)
        self.seqr = ConfigDB().get(None, "", "SEQR")

    async def body(self):
        prev_num = 0
        cur_num = 1
        fib_list = [prev_num, cur_num]

        for _ in range(7):
            sum = await do_add(self.seqr, prev_num, cur_num)
            fib_list.append(sum)
            prev_num = cur_num
            cur_num = sum

        uvm_root().logger.info("Fibonacci Sequence: " + str(fib_list))
