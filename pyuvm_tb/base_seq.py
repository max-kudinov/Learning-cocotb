from pyuvm import uvm_sequence
import sys

from alu_seq_item import AluSeqItem
sys.path.insert(0, "..")
from tinyalu_utils import Ops  # noqa: E402


class BaseSeq(uvm_sequence):
    async def body(self):
        for op in list(Ops):
            cmd_tr = AluSeqItem("cmd_tr", 0, 0, op)
            await self.start_item(cmd_tr)
            self.set_operands(cmd_tr)
            await self.finish_item(cmd_tr)
