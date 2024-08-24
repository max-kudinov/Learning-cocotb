from pyuvm import uvm_sequence
import sys

from alu_seq_item import AluSeqItem
sys.path.insert(0, "..")
from tinyalu_utils import Ops  # noqa: E402


class OpSeq(uvm_sequence):
    def __init__(self, name, a, b, op):
        super().__init__(name)
        self.a = a
        self.b = b
        self.op = Ops(op)

    async def body(self):
        seq_item = AluSeqItem("seq_item", self.a, self.b, self.op)
        await self.start_item(seq_item)
        await self.finish_item(seq_item)
        self.result = seq_item.result
